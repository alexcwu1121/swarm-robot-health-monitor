from comms import Comms
import sys
import interface as inter
import json
import time
from Service import Service
from comms import Message

class ThresholdAnalytic(Service):

    def init_config(self, service_conf):
        # TODO: don't hardcode this config file. get it from gui
        with open("config/config_testing_c.json") as f:
            self.config = json.load(f)

        # TODO: don't hardcode this config file. get it from gui
        with open("config/config_threshold.json") as f:
            self.analytic_config = json.load(f)

        self.bounds = {}
        self.bounds['global'] = self.analytic_config['Threshold']['bounds']['global']

        # Connect to robots
        for item in self.config['mlist']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['ip'])
            self.state[item['ip']] = dict()
            for key in item['data'].keys():
                self.state[item['ip']][key] = [0]

        # Connect to analytics according to config
        ip = self.analytic_config['Threshold']['publish']['ip']
        port = self.analytic_config['Threshold']['publish']['port']
        self.comms.add_publisher_port(ip, port, 'Threshold')

        time.sleep(0.5)

    def update_options(self):
        pass

    def transform(self):
        for ip in self.state.keys():
            # Check status data
            msg_recv = self.comms.get(ip)
            if msg_recv is not None:
                for key in msg_recv.payload.keys():
                    self.state[ip][key] = [msg_recv.payload[key]]
        return

    # take a threshold dictionary and a robot's current state and return threshold condition for each sensor
    def within_threshold(self, bounds, state):
        threshold = {}
        for sensor in state.keys():
            # If the data isn't a string, assume threshold satisfied
            try:
                float(state[sensor][0])
            except ValueError:
                threshold[sensor] = True
                continue

            if sensor in bounds.keys():
                if float(bounds[sensor]['min']) < float(state[sensor][0]) < float(bounds[sensor]['max']):
                    threshold[sensor] = True
                else:
                    threshold[sensor] = False
            else:
                # If no bounds imposed on a sensor, threshold satisfied
                threshold[sensor] = True
        return threshold

    def run(self):
        while True:
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