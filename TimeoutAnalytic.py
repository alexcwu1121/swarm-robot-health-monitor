"""
The timeout analytic detects if a machine has been unresponsive for too long
and makes the neccessary changes to the display
"""

import sys
import json
import time
from Service import Service
from comms import Message

class TimeoutAnalytic(Service):

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
        with open("config/config_timeout.json") as f:
            self.analytic_config = json.load(f)

        self.timeout = float(self.analytic_config['Timeout']['timeout'])

        # Set up subscribers according to config
        for item in self.analytic_config['Timeout']['subscribe']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['topic'])

        # Set up publisher according to config
        ip = self.analytic_config['Timeout']['publish']['ip']
        port = self.analytic_config['Timeout']['publish']['port']
        self.comms.add_publisher_port(ip, port, 'Timeout')

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
        """
        self.state[item['ip']] = dict()
        self.state[item['ip']]["Timeout"] = 0
        self.state[item['ip']]["PrevTime"] = time.process_time()
        """
        for topic in self.comms.subscriber_ports.keys() - self.state.keys():
            msg_recv = self.comms.get(topic)
            if msg_recv is not None:
                if msg_recv.topic not in self.state.keys():
                    self.state[msg_recv.topic] = dict()
                self.state[msg_recv.topic]["PrevTime"] = time.process_time()
        return

    """
    Runs the timeout analytic
    Return: 
        None
    """
    def run(self):
        while True:
            # update state and transform data
            self.transform()
            for ip in self.state.keys():
                time_elapsed = time.process_time() - self.state[ip]["PrevTime"]
                timeout = {"Timeout": True}
                if time_elapsed > self.timeout:
                    timeout["Timeout"] = False
                self.comms.send("Timeout", Message(ip, timeout))


if __name__ == "__main__":
    timeout = TimeoutAnalytic()
    timeout.run()