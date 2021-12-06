

import sys
import json
import time
from Service import Service
from comms import Message

class ThresholdAnalytic(Service):

    """
    Initiates the configuration for the service
    Attributes:
        service_conf: Dict()
            The configuration for the service
    Return: 
        None
    """
    def init_config(self, service_conf):
        # TODO: don't hardcode this config file. get it from gui
        with open("config/config_testing_c.json") as f:
            self.config = json.load(f)

        # TODO: don't hardcode this config file. get it from gui
        with open("config/config_threshold.json") as f:
            self.analytic_config = json.load(f)

        self.bounds = {}
        self.bounds['global'] = self.analytic_config['Threshold']['bounds']['global']

        # Set up subscribers according to config
        for item in self.analytic_config['Threshold']['subscribe']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['topic'])

        # Connect to analytics according to config
        ip = self.analytic_config['Threshold']['publish']['ip']
        port = self.analytic_config['Threshold']['publish']['port']
        self.comms.add_publisher_port(ip, port, 'Threshold')

        time.sleep(0.5)

    """
    This will update the parameters for the service
    Return: 
        None
    """
    def update_options(self):
        pass

    """
    Transforms a message to a state and stores it in the object for later reference
    Return: 
        None
    """
    def transform(self):
        for topic in self.comms.subscriber_ports.keys():
            msg_recv = self.comms.get(topic)
            if msg_recv is not None:
                if msg_recv.topic in self.state.keys():
                    self.state[msg_recv.topic].update(msg_recv.payload)
                else:
                    self.state[msg_recv.topic] = msg_recv.payload
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

    """
    Runs the threshold analytic
    Return: 
        None
    """
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