# Empowering Network Automation

[![Run in Cisco Cloud IDE](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-runable-icon.svg)](https://developer.cisco.com/codeexchange/devenv/jillesca/DEVWKS-3551/)

Welcome to **DEVWKS-3551 Empowering Network Automation, Practice NSO with Python**

This file provides the instructions you'll need for the workshop. However, don't feel restricted to the workshop timeline. Feel free to explore and try out the exercises at your own pace. Simply click on the **_Cisco Cloud IDE Run it!_** button located at the top left corner to get started at any time.

For your convenience, all the information shared during the workshop is compiled in the [NSO Python API](NSO_Python_API.md) markdown file. Consider it your go-to resource for reference.

## Objective

Start on a hands-on journey to learn the NSO Python API. We've designed this workshop around the concept of **_learning by fixing_**. You'll dive into broken examples, unravel the issues, and learn how to navigate the Python API in the process.

This approach not only gives you practical experience but also equips you with the problem-solving skills needed in real-world programming. Get ready to transform challenges into learning opportunities.

## Setup the environment

Setup the environment required for the lab.

```bash
cd ~/src/DEVWKS-3551/
```

```bash
make
```

> [!NOTE]
> If you receive an error during the setup, enter `make` again. If there are too many issues, reset the environment.

If you're curious to see the working examples, feel free to explore the files in the [the answer](answers/) directory. Alternatively, if you're ready to test your skills, you can replace the problematic files with the correct ones and see if they work as expected.

## Scenario 1. Scripting with the NSO Python API

Our first scenario offers a straightforward example of how to change a device's hostname using the _Python NSO API_, providing a hands-on opportunity to familiarize yourself with its interaction.

To identify the problem, you can either debug the code or utilize the helper functions embedded in the script, designed to simplify error detection.

Start by running the [ncs_scripting.py file.](scripting/ncs_scripting.py)

```bash
python ~/src/DEVWKS-3551/scripting/ncs_scripting.py
```

You can also get the same data via RESTCONF

```bash
python ~/src/DEVWKS-3551/scripting/restconf_scripting.py
```

## Scenario 2. Run services with NSO Python API

This example showcases an NSO service that use Python to simplify templates, making them easier to maintain.

> [!NOTE]
> Work with the files under the [packages/router](packages/router/) directory. This package has a symbolic link to the running NSO packages directory.

### Prepare the example

First compile the package used.

```bash
make clean all -C ${NCS_RUN_DIR}/packages/router/src/
```

Reload the packages.

```bash
echo "packages reload" | ncs_cli -C -u admin
```

### Test the example

Test if the package works correctly.

```bash
ncs_cli -Cu admin
```

```bash
config
```

Pick any one or multiple lines below to test the router package.

```bash
router core device core-rtr0 sys dns server 1.1.1.1
router core device core-rtr0 sys syslog server 1.1.1.1
router core device core-rtr0 sys syslog server 2.2.2.2
router core device core-rtr0 sys ntp server 1.1.1.1
router core device core-rtr0 sys ntp server 2.2.2.2
router distribution device dist-rtr0 sys dns server 6.6.6.6
router distribution device dist-rtr0 sys dns server 5.5.5.5
router distribution device dist-rtr0 sys syslog server 6.6.6.6
router access device dist-sw0 sys dns server 4.4.4.4
router access device dist-sw0 sys dns server 3.3.3.3
router access device dist-sw0 sys syslog server 4.4.4.4
router access device dist-sw0 sys syslog server 3.3.3.3
router access device dist-sw0 sys ntp server 4.4.4.4
router access device dist-sw0 sys ntp server 3.3.3.3
```

Do a `dry-run` to make sure the package is working correctly.

```bash
commit dry-run
```

> [!NOTE]
> If issues, review the [router python script](packages/router/python/router/router.py) under the packages directoy.

Redeploy the package if you make changes to the python script.

```bash
packages package router redeploy
```

Test the package again with a `commit dry-run`

Finally, when the package is fixed, commit the changes.

```bash
commit
```

## Scenario 3. Interact with NSO programmatically

Interact with NSO adding a new DNS server using the `RESTCONF` interface, which is useful when integrating NSO with external systems.

Use the [restconf_service.py](scripting/restconf_service.py) file. On this example the `http` code is already correctly implemented.

```bash
python ~/src/DEVWKS-3551/scripting/restconf_service.py
```

### Appendix. Useful commands

Access netsim cli device.

```bash
ncs-netsim cli-c core-rtr0 --dir ~/src/workshop/netsim
show running-config hostname
```

Use show commands using live-status on NSO.

```bash
devices device core-rtr0 live-status exec show running-config hostname
```

Redeploy the router packages for changes on python code or templates files.

```bash
echo 'packages package router redeploy' | ncs_cli -Cu admin
```
