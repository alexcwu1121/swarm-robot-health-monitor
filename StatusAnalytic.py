import sys
import json
import time
from Service import Service
from comms import Message
from comms import Comms

class StatusAnalytic(Service):

    def __init__(self):
        self.comms = Comms()
        self.state = {}
        self.services = []
        self.conditions = {}

        try:
            with open("config/service_config.json") as f:
                config = json.load(f)
                self.comms.add_publisher_port(config["Status"]["ip"],
                                                config["Status"]["port"],
                                                "Status")
                self.comms.add_subscriber_port(config["Dispatcher"]["ip"],
                                                config["Dispatcher"]["port"],
                                                "Dispatcher")
                self.comms.add_subscriber_port(config["Timeout"]["ip"],
                                                config["Timeout"]["port"],
                                                "Timeout")
                self.comms.add_subscriber_port(config["Threshold"]["ip"],
                                                config["Threshold"]["port"],
                                                "Threshold")
                self.services.append("Timeout")
                self.services.append("Threshold")
        except:
            print("Service Config error!")
            exit(1)

        time.sleep(0.5)

    def set_config(self, config):
        self.state.clear()
        self.conditions.clear()
        self.conditions = config["alist"]["conditions"]
        for robot in config["mlist"]:
            self.state[robot["ip"]] = {}
        time.sleep(0.5)


    # def init_config(self, service_conf):
    #     # TODO: don't hardcode this config file. get it from gui
    #     with open("config/config_status.json") as f:
    #         self.analytic_config = json.load(f)

    #     self.status_conditions = self.analytic_config['Status']['conditions']

    #     # Set up subscribers according to config
    #     for item in self.analytic_config['Status']['subscribe']:
    #         self.comms.add_subscriber_port(item['ip'], item['port'], item['topic'])

    #     # Set up publisher according to config
    #     ip = self.analytic_config['Status']['publish']['ip']
    #     port = self.analytic_config['Status']['publish']['port']
    #     self.comms.add_publisher_port(ip, port, 'Status')

    #     time.sleep(0.5)

    # def update_options(self):
    #     pass

    def transform(self):
        for sub in self.services:
            msg = self.comms.get(sub)
            if msg is not None:
                self.state[msg.topic].update(msg.payload)
        return

    def get_status(self, state):
        status = {}

        # if timeout specifically fails, then immediate critical
        if not state['Timeout']:
            status["Status"] = "disconnected"
            return status

        values = list(state.values())
        failures = len(values) - sum(values)

        if failures <= int(self.conditions["nominal"]):
            status["Status"] = "nominal"
        elif failures <= int(self.conditions["warning"]):
            status["Status"] = "warning"
        else:
            status["Status"] = "critical"
        return status

    def run(self):
        while True:

            try:
                msg = self.comms.get("Dispatcher")
                if msg is not None:
                    print("got config in status")
                    self.set_config(msg.payload)
            except KeyError:
                pass

            if(not self.state):
                continue

            # update state and transform data
            self.transform()
            for ip in self.state.keys():
                try:
                    status = self.get_status(self.state[ip])
                    self.comms.send("Status", Message(ip, status))
                except KeyError:
                    pass
            


if __name__ == "__main__":
    status = StatusAnalytic()
    status.run()