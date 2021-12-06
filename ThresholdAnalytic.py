import sys
import json
import time
from Service import Service
from comms import Comms
from comms import Message

class ThresholdAnalytic(Service):

    def __init__(self):

        self.comms = Comms()
        self.services = []
        self.state = {}
        self.bounds = {}

        try:
            with open("config/service_config.json") as f:
                config = json.load(f)
                self.comms.add_publisher_port(config["Threshold"]["ip"],
                                                config["Threshold"]["port"],
                                                "Threshold")
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
        self.bounds.clear()
        self.bounds['global'] = config["alist"]["Threshold"]["bounds"]["global"]
        for robot in config["mlist"]:
            ip = robot["ip"]
            self.state[ip] = {}
            for sensor in robot["data"].keys():
                self.state[ip][sensor] = ""
        time.sleep(0.5)
        

    # def init_config(self, service_conf):
    #     # TODO: don't hardcode this config file. get it from gui
    #     with open("config/config_testing_c.json") as f:
    #         self.config = json.load(f)

    #     # TODO: don't hardcode this config file. get it from gui
    #     with open("config/config_threshold.json") as f:
    #         self.analytic_config = json.load(f)

    #     self.bounds = {}
    #     self.bounds['global'] = self.analytic_config['Threshold']['bounds']['global']

    #     # Set up subscribers according to config
    #     for item in self.analytic_config['Threshold']['subscribe']:
    #         self.comms.add_subscriber_port(item['ip'], item['port'], item['topic'])

    #     # Connect to analytics according to config
    #     ip = self.analytic_config['Threshold']['publish']['ip']
    #     port = self.analytic_config['Threshold']['publish']['port']
    #     self.comms.add_publisher_port(ip, port, 'Threshold')

    #     time.sleep(0.5)

    def update_options(self):
        pass

    def transform(self):
        # Check for new message from all sevices and update internal state
        for sub in self.services:
            msg = self.comms.get(sub)
            if msg is not None:
                self.state[msg.topic].update(msg.payload)
        return

    # take a threshold dictionary and a robot's current state and return threshold condition for each sensor
    def within_threshold(self, bounds, state):
        threshold = {}
        for sensor in state.keys():
            # If the data isn't a string, assume threshold satisfied
            try:
                float(state[sensor])
            except ValueError:
                threshold[sensor] = True
                continue

            if sensor in bounds.keys():
                if float(bounds[sensor]['min']) <= float(state[sensor]) <= float(bounds[sensor]['max']):
                    threshold[sensor] = True
                else:
                    threshold[sensor] = False
            else:
                # If no bounds imposed on a sensor, threshold satisfied
                threshold[sensor] = True
        return threshold

    def run(self):
        while True:

            try:
                msg = self.comms.get("Dispatcher")
                if msg is not None:
                    print("got config in threshold")
                    self.set_config(msg.payload)
            except KeyError:
                pass

            if (not self.state):
                continue
            # update state and transform data
            self.transform()

            # Compute and publish thresholds for each robot
            # Specific thresholds take precedence over global thresholds
            for ip in self.state.keys():
                threshold = self.within_threshold(self.bounds['global'], self.state[ip])
                self.comms.send("Threshold", Message(ip, threshold))


if __name__ == "__main__":
    threshold = ThresholdAnalytic()
    threshold.run()