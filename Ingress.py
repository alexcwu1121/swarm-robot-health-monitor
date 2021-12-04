import sys
import json
import time
from Service import Service
from comms import Message
from comms import Comms

class Ingress(Service):

    def __init__(self):
        
        self.comms = Comms()
        self.state = {}

        try:
            with open("config/service_config.json") as f:
                config = json.load(f)
                self.comms.add_publisher_port(config["Ingress"]["ip"],
                                                config["Ingress"]["port"],
                                                "Ingress")
                self.comms.add_subscriber_port(config["Dispatcher"]["ip"],
                                                config["Dispatcher"]["port"],
                                                "Dispatch")
        except:
            print("Service Config error!")
            exit(1)

        time.sleep(0.5)

    def set_config(self, config):

        self.state.clear()

        # Connect to robots
        for r in config['mlist']:
            self.comms.add_subscriber_port(r['ip'], r['port'], r['ip'])
            self.state[r['ip']] = {}
        time.sleep(0.5)

    # def update_options(self):
    #     pass

    def transform(self):
        for ip in self.comms.subscriber_ports.keys():
            # Check status data
            msg_recv = self.comms.get(ip)
            if msg_recv is not None:
                self.state[ip] = msg_recv
        return

    def run(self):
        while True:

            try:
                msg = self.comms.get("Config")
                if msg is not None:
                    self.set_config(msg.payload)
            except KeyError:
                pass

            if(not self.state):
                continue

            # update states for all robots
            try:
                self.transform()
            except KeyError:
                pass

            # Send a message for each robot state
            for ip in self.state.keys():
                self.comms.send("Ingress", self.state[ip])

if __name__ == "__main__":
    ingress = Ingress()
    ingress.run()