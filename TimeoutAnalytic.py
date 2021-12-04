import sys
import json
import time
from Service import Service
from comms import Message
from comms import Comms

class TimeoutAnalytic(Service):

    def __init__(self):

        self.comms = Comms()
        self.services = []
        self.state = {}

        try:
            with open("config/service_config.json") as f:
                config = json.load(f)
                self.comms.add_publisher_port(config["Timeout"]["ip"],
                                                config["Timeout"]["port"],
                                                "Timeout")
                self.comms.add_subscriber_port(config["Dispatcher"]["ip"],
                                                config["Dispatcher"]["port"],
                                                "Dispatcher")
                self.comms.add_subscriber_port(config["Ingress"]["ip"],
                                                config["Ingress"]["port"],
                                                "Ingress")
                self.services.append("Ingress")
        except:
            print("Service Config error!")
            exit(1)

        time.sleep(0.5)

    def set_config(self, config):
        self.state.clear()
        for robot in config["mlist"]:
            self.state[robot["ip"]] = {}
            self.state[robot["ip"]]["PrevTime"] = time.process_time()
        self.timeout = float(config["alist"]["timeout"])

        time.sleep(0.5)


    # def init_config(self, service_conf):

    #     self.timeout = float(self.analytic_config['Timeout']['timeout'])

    #     # Set up subscribers according to config
    #     for item in self.analytic_config['Timeout']['subscribe']:
    #         self.comms.add_subscriber_port(item['ip'], item['port'], item['topic'])

    #     # Set up publisher according to config
    #     ip = self.analytic_config['Timeout']['publish']['ip']
    #     port = self.analytic_config['Timeout']['publish']['port']
    #     self.comms.add_publisher_port(ip, port, 'Timeout')

    #     time.sleep(0.5)

    # def update_options(self):
    #     pass

    def transform(self):
        """
        self.state[item['ip']] = dict()
        self.state[item['ip']]["Timeout"] = 0
        self.state[item['ip']]["PrevTime"] = time.process_time()
        """
        for sub in self.services:
            msg_recv = self.comms.get(sub)
            if msg_recv is not None:
                self.state[msg_recv.topic]["PrevTime"] = time.process_time()
        return

    def run(self):
        while True:

            try:
                msg = self.comms.get("Dispatcher")
                if msg is not None:
                    print("got config in timeout")
                    self.set_config(msg.payload)
            except KeyError:
                pass

            if (not self.state):
                continue
            # update state and transform data
            try:
                self.transform()
            except KeyError:
                pass

            for ip, values in self.state.items():
                time_elapsed = time.process_time() - values["PrevTime"]
                timeout = {"Timeout": True}
                if time_elapsed > self.timeout:
                    timeout["Timeout"] = False
                self.comms.send("Timeout", Message(ip, timeout))


if __name__ == "__main__":
    timeout = TimeoutAnalytic()
    timeout.run()