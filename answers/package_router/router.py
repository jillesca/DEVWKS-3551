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

        for server in service.sys.dns.server:
            vars.add("DNS_ADDRESS", server.address)
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
