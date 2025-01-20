import ncs


def update_device_attribute_dry_run(device_name: str, hostname: str) -> dict:
    with ncs.maapi.single_write_trans(
        user="admin", context="system"
    ) as transaction:
        root = ncs.maagic.get_root(backend=transaction)
        root.devices.device[device_name].hostname = hostname

        commit_params = transaction.get_params()
        commit_params.dry_run_native()
        dry_run_result = transaction.apply_params(
            keep_open=True, params=commit_params
        )
        print(f"{dry_run_result=}")


# TIP: See the attributes of the device object
def update_device_attribute(device_name: str, hostname: str) -> None:
    with ncs.maapi.single_write_trans(
        user="admin", context="system"
    ) as transaction:
        root = ncs.maagic.get_root(backend=transaction)
        root.devices.device[device_name].config.hostname = hostname
        transaction.apply()
        print("Transaction applied")


def see_object_attributes() -> None:
    maapi = ncs.maapi.Maapi()
    maapi.start_user_session(user="admin", context="system", groups=[])
    transaction = maapi.start_write_trans()

    root = ncs.maagic.get_root(backend=transaction)
    for device in root.devices.device:
        print("#" * 50)
        print(dir(device))
    maapi.close()


def see_device_address() -> None:
    maapi = ncs.maapi.Maapi()
    maapi.start_user_session(user="admin", context="system", groups=[])
    transaction = maapi.start_write_trans()

    root = ncs.maagic.get_root(backend=transaction)
    for device in root.devices.device:
        print(f"Device {device.name} address {device.address}")
        print(f"{dir(device.config)=}")
    maapi.close()


def show_xr_command(device_name: str, show_command: str) -> None:
    with ncs.maapi.Maapi() as maapi:
        with ncs.maapi.Session(maapi=maapi, user="admin", context="system"):
            root = ncs.maagic.get_root(backend=maapi)
            device = root.devices.device[device_name]
            cli_any_command = device.live_status.cisco_ios_xr_stats__exec.show
            command = cli_any_command.get_input()
            command.args = [show_command]
            result = cli_any_command.request(command)
            print(result.result)


def get_device_hostname(device_name: str) -> None:
    with ncs.maapi.single_read_trans(
        user="admin", context="system"
    ) as transaction:
        root = ncs.maagic.get_root(backend=transaction)
        device = root.devices.device[device_name]
        result = device.config.hostname
        print(f"{result=}")


if "__main__" == __name__:

    HOSTNAME = "devwks-3551"
    DEVICE_NAME = "core-rtr0"

    # see_object_attributes()

    # see_device_address()

    update_device_attribute_dry_run(device_name=DEVICE_NAME, hostname=HOSTNAME)

    update_device_attribute(device_name=DEVICE_NAME, hostname=HOSTNAME)

    # show_xr_command(
    #     device_name=DEVICE_NAME, show_command="running-config hostname"
    # )

    # get_device_hostname(device_name=DEVICE_NAME)
