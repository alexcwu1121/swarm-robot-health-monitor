"""
Listens to all robots in the swarm and collapses the data into a single stream
"""

import sys
import json
import time
from Service import Service
from comms import Message

class Ingress(Service):

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
        with open("config/config_ingress.json") as f:
            self.analytic_config = json.load(f)

        # Connect to robots
        for item in self.config['mlist']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['ip'])

        # Set up publisher port for merged robot messages
        ip = self.analytic_config['Ingress']['publish']['ip']
        port = self.analytic_config['Ingress']['publish']['port']
        self.comms.add_publisher_port(ip, port, 'Ingress')

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
        for ip in self.comms.subscriber_ports.keys():
            # Check status data
            msg_recv = self.comms.get(ip)
            if msg_recv is not None:
                self.state[ip] = msg_recv
        return

    """
    Runs the ingress analytic
    Return: 
        None
    """
    def run(self):
        while True:
            # update states for all robots
            self.transform()

            # Send a message for each robot state
            for ip in self.state.keys():
                self.comms.send("Ingress", self.state[ip])


if __name__ == "__main__":
    ingress = Ingress()
    ingress.run()