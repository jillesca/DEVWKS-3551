# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


class ServiceCallbacks(Service):

    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info("Service create(service=", service._path, ")")

        device_name = root.devices.device[service.device].name
        self.log.info(f"Configuring device {device_name}")

        vars = ncs.template.Variables()
        template = ncs.template.Template(service)

        # TIPs:
        # Compare the python object to its corresponding yang model under the src/yang folder
        # see the python logs at $NCS_RUN_DIR/logs to see the line with error

        for server in service.sys.dns.servers:
            vars.add("DNS_ADDRESS", server.host)
            template.apply("dns-template", vars)

        for server in service.sys.syslog.server:
            vars.add("SYSLOG_ADDRESS", server.name)
            template.apply("syslog-template", vars)

        for server in service.sys.ntp.server:
            vars.add("NTP_ADDRESS", server.name)
            template.apply("ntp-template", vars)


class Router(ncs.application.Application):
    def setup(self):
        self.log.info("Router RUNNING")
        self.register_service("router-servicepoint", ServiceCallbacks)

    def teardown(self):
        self.log.info("Router FINISHED")
