# NSO Python API/SDK

- The NSO Python, Java, Erlang (and C) APIs are **SDKs** used to extend NSO.
- Typically used by applications running on the same processor/system as NSO is running.
- Uses IPC over TCP sockets to communicate with NSO for low latency.
- Not available via `pip install`

_Reference._

- <https://developer.cisco.com/docs/nso/api/nso-sdk-api-reference/>

## Development

| Scripts                                     | Services                                                       |
| ------------------------------------------- | -------------------------------------------------------------- |
| Connect directly to NSO datastore.          | Perform complex calculations & external system - integrations. |
| Onetime operations.                         | Apply XML templates from Python.                               |
| Importing device configurations.            | Get FASTMAP algorithm benefits.                                |
| Generating reports from the configurations. |                                                                |

## High-level & Low-level APIs

- Low-level APIs are a direct mapping of the NSO C APIs, CDB and MAAPI.
  - See man `confd_lib_lib` for more information.
- High-level APIs are an abstraction layer on top of the low-level APIs.
  - Easier to use.
  - Improved code readability and development for common use cases.

_Reference._

- <https://cisco-tailf.gitbook.io/nso-docs/development/core-concepts/api-overview/python-api-overview>
- <https://cisco-tailf.gitbook.io/nso-docs/resources/index#section-3-c-library-functions>

## MAAPI API

Management Agent API

- Transactional Northbound interface.
- User session-based interface.
- Configuration & Operational data
  - Read.
  - Written and committed as one transaction.

```python
import ncs

with ncs.maapi.Maapi() as maapi:
    with ncs.maapi.Session(maapi=maapi, user="admin", context="system"):
        with maapi.start_read_trans() as transaction:
            address = transaction.get_elem("/ncs:devices/device{ex0}/address")
            print("First read: Address = %s" % address)

with ncs.maapi.single_write_trans(user="admin", context="system") as transaction:
    transaction.set_elem2("Vegas was here", "/ncs:devices/device{ex0}/description")
    transaction.apply()

```

```python
# Access list item
router = root.devices.device["internet-rtr0"]

# Create list item
root.services.l3vpn.create("test-l3vpn")

# Check if list item with a key exists
"internet-rtr0" in root.devices.device

# Set leaf value
root.devices.device["internet-rtr0"].address = "10.0.0.1"

# Remove list item
del root.devices.device["internet-rtr0"]
```

_Reference._

- <https://cisco-tailf.gitbook.io/nso-docs/development/core-concepts/api-overview/python-api-overview>

## MAAGIC API

- Manipulate data according to YANG schema
- Use standard Python object dot notation.
- Special characters are replaced with underscores
- Element `my-address` becomes `my_address`
  - Crossing Namespaces with _double-underscore_
    - `root.myns__top.val`

> MAAGIC = Management Agent API (MAAPI) + magic Python methods

_Reference._

- <https://cisco-tailf.gitbook.io/nso-docs/development/core-concepts/api-overview/python-api-overview#maagic-api>

### MAAGIC Object Navigation

| Action                                       | Object Returned   |
| -------------------------------------------- | ----------------- |
| `root.devices`                               | Container         |
| `root.devices.device`                        | List              |
| `root.devices.device["ce0"]`                 | ListElement       |
| `root.devices.device['ce0'].device_type.cli` | PresenceContainer |
| `root.devices.device['ce0'].address`         | str               |
| `root.devices.device['ce0'].port`            | int               |

Maagic object from a keypath:

`node = ncs.maagic.get_node(transaction_id, '/ncs:devices/device{ce0}')`

_Reference._

- <https://cisco-tailf.gitbook.io/nso-docs/development/core-concepts/api-overview/python-api-overview#maagic-api>
- <https://developer.cisco.com/docs/nso/api/ncs-maagic/>

## Transactions and Commits

- Use Python Context Managers (the `with` key word)
- Transactions are closed by default after they are applied
- Commit options can be specified
- You only need to create a write transactions for actions, not services

```python
import ncs

with ncs.maapi.Maapi() as m:
    with ncs.maapi.Session(m, "admin", "python", groups=["ncsadmin"]):
        with m.start_write_trans() as t_rw:

            root = ncs.maagic.get_root(t_rw)
            device_cdb = root.devices.device["eng04-cleaf-02"]
            device_cdb.config.interface.loopback[0].description = ("Done from python API")

            # Starting dry-run
            cp = ncs.maapi.ConfigParams()
            cp.dry_run_native()
            dry_run_result = t_rw.apply_params(True, cp)
```

## Navigate the API

### Python `help()` function

```python
>>> import ncs
>>> with ncs.maapi.single_write_trans(user="admin", context="system") as transaction:
... root = ncs.maagic.get_root(transaction)
... devices = root.devices
...
>>> help(devices)
```

Will result:

```bash
Help on Container in module ncs.maagic object:

class Container(Node)
 |  Container(backend, cs_node, parent=None)
 |
 |  Represents a yang container.
 |
 |  A (non-presence) container node or a list element, contains other nodes.
 |
 |  Method resolution order:
 |      Container
 |      Node
 |      builtins.object
 |
 |  Methods defined here:
 |
 |  __init__(self, backend, cs_node, parent=None)
 |      Initialize Container node. Should not be called explicitly.
 |
 |  __repr__(self)
 |      Get internal representation.
...
```

### ncs_pycli

```python
In [1]: for device in root.ncs__devices.device:
...: print(device.name)
...:
ce0
ce1

In [2]: device = root.ncs__devices.device['ce0']

In [3]: type(device)
Out[3]: ncs.maagic.ListElement

In [4]: device
Out[4]: ListElement name=device tag=617911018 keys={ce0}

In [5]: help(device)

In [6]: device.
device.active_settings
device.address
```

_Reference._

- <https://github.com/NSO-developer/ncs_pycli>

### Documentation

- <https://cisco-tailf.gitbook.io/nso-docs/development/core-concepts/api-overview/python-api-overview>
- <https://developer.cisco.com/docs/nso/api/ncs/#package-ncs>
- <https://cisco-tailf.gitbook.io/nso-docs/resources/index/section3#confd_lib_maapi>

### Maagic with Devtools

```python
admin@ncs# devtools true
admin@ncs# show running-config devices device ex0 | display maagic
root.ncs__devices.device['ex0'].address 127.0.0.1
root.ncs__devices.device['ex0'].port 12022
root.ncs__devices.device['ex0'].authgroup default
root.ncs__devices.device['ex0'].device-type.netconf.ned-id ne-nc-1.0
root.ncs__devices.device['ex0'].config.aaa__aaa.authentication.users.user['admin']
root.ncs__devices.device['ex0'].config.aaa__aaa.authentication.users.user['oper']
```

```python
admin@ncs# config
Entering configuration mode terminal
admin@ncs(config)# devices device ex0 port 10233
admin@ncs(config-device-ex0)# top
admin@ncs(config)# show configuration | display maagic
root = ncs.maagic.get_root(t)
root.ncs__devices.device['ex0'].port = '10233'
```

_Reference._

- <https://cisco-tailf.gitbook.io/nso-docs/operation-and-usage/cli/introduction-to-nso-cli#d5e1541>

### Logs

- `tailf-ncs-python-vm.yang` & `ncs.conf` define the python-vm container.
  - See example 26: _The Python VM YANG model_ for full explanation.
- Some of `python-vm` nodes are by default invisible.
  - See documentation for xml and cli command needed.
- Filename: `logs/ncs-python-vm-<package-name>.log` by default.

_Reference._

- <https://cisco-tailf.gitbook.io/nso-docs/development/core-concepts/nso-virtual-machines/nso-python-vm>

### Debug

- Python packages run without an attached console.
  - Standard output collected in `ncs-python-vm.log`
- Python APIs provide logging objects based on the standard Python logging module.
- Default logging level set to info.

```bash
$ ncs_cli -u admin
admin@ncs> config
admin@ncs% set python-vm logging level level-debug
admin@ncs% commit
```

## Services with Python

Registering a service.

```python
from ncs.application import Application
from ncs.application import Service
import ncs.template

class ServiceCallbacks(Service):
  @Service.create
  def cb_create(self, tctx, root, service, proplist):
    self.log.info('Service create(service=', service._path, ')')
    # Add the service logic

class Service(Application):
  def setup(self):
    self.log.info('Worker RUNNING')
    self.register_service('service-servicepoint', ServiceCallbacks)
  def teardown(self):
    self.log.info('Worker FINISHED')
```

Adding custom logic.

```python
class ServiceCallbacks(Service):
  @Service.create
  def cb_create(self, tctx, root, service, proplist):
    self.log.info('Service create(service=', service._path, ')')

    # Add the service logic >>>>>>>
    vars = ncs.template.Variables()
    vars.add('MAGIC', '42')
    vars.add('CE', service.device)
    vars.add('INTERFACE', service.unit)
    template = ncs.template.Template(service)
    template.apply('pyservice-template', vars)

    self.log.info('Template is applied')

    dev = root.devices.device[service.device]
    dev.description = "This device was modified by %s" % service._path
```

Pre and Post modifications.

```python
class ServiceCallbacks(Service):

  @Service.create
  def cb_create(self, tctx, root, service, proplist):
    self.log.info('Service create(service=', service._path, ')')

  @Service.pre_modification
  def cb_pre_modification(self, tctx, op, kp, root, proplist):
    self.log.info('Service premod(service=', kp, ')')

  @Service.post_modification
  def cb_post_modification(self, tctx, op, kp, root, proplist):
    self.log.info('Service premod(service=', kp, ')')
```

_Reference._

- <https://cisco-tailf.gitbook.io/nso-docs/development/core-concepts/api-overview/python-api-overview#d5e4639>

## Nano Services

- Reactive FASTMAP (RFM)
- Provide provisioning steps.
- Handle side-effects, useful for working with external systems.

_Reference._

- <https://cisco-tailf.gitbook.io/nso-docs/development/core-concepts/nano-services>

## More Resources

Check the NSO Example Collection online at <https://github.com/NSO-developer/nso-examples>

Or inside your NSO system.

```bash
find $NCS_DIR/examples.ncs/ -name "*.py" | grep -v "__init__.py"
```

## Call to Action

Continue your learning journey

- Expand your knowledge
  - <https://cisco-tailf.gitbook.io/nso-docs/development/core-concepts/api-overview/python-api-overview>
- Practice the NSO Python API
  - <https://developer.cisco.com/learning/labs/service-dev-201/introduction>
- Get started with NSO
  - <https://developer.cisco.com/learning/tracks/get_started_with_nso>
- Review best practices for service development
  - <https://github.com/NSO-developer/nso-service-dev-practices>
