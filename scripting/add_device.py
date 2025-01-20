import argparse
import ncs


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", help="device name", required=True)
    parser.add_argument("--address", help="device address", required=True)
    parser.add_argument("--ned", help="device NED ID", required=True)
    parser.add_argument("--port", help="device port", type=int, default=22)
    parser.add_argument(
        "--desc",
        help="device description",
        default="Device created by maagic_create_device.py",
    )
    parser.add_argument("--auth", help="device authgroup", default="default")
    return parser.parse_args()


def main(args):
    with ncs.maapi.Maapi() as maapi:
        with ncs.maapi.Session(maapi=maapi, user="admin", context="system"):
            with maapi.start_write_trans() as transaction:
                print(f'Setting the device "{args.name}" configuration...')

                # Get a reference to the device list
                root = ncs.maagic.get_root(backend=transaction)
                device_list = root.devices.device

                if args.name not in device_list:
                    device = device_list.create(args.name)
                    device.port = args.port
                    device.authgroup = args.auth
                    device.address = args.address
                    device.description = args.desc
                    dev_type = device.device_type.cli
                    dev_type.ned_id = args.ned
                    device.state.admin_state = "unlocked"

                    print("Committing the device configuration...")
                    transaction.apply()
                    print("Device committed!")
                else:
                    print(
                        f'Device "{args.name}" configuration already exists...'
                    )

            # This transaction is no longer valid - since we are moving
            # back under ncs.maapi.Session(m, 'admin', 'python')

            # fetch-host-keys and sync-from does not require a
            # transaction, continue using the Maapi object
            root = ncs.maagic.get_root(backend=maapi)
            device = root.devices.device[args.name]
            print("Fetching SSH keys...")
            output = device.ssh.fetch_host_keys()
            print(f"Result: {output.result}")
            print("Syncing configuration...")
            output = device.sync_from()
            print(f"Result: {output.result}")
            if not output.result:
                print(f"Error: {output.info}")


if __name__ == "__main__":
    main(parse_args())
