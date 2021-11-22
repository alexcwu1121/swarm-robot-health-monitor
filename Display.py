"""
Display.py
manages the server's connections to all the robots in the swarm
    - creates a subscriber for every robot in the swarm 
    - tracks the latest updates from the robots
    - maintains an internal dictonary that is updated whenever a new message is sent to the server from a robot
"""

from comms import Comms
import json
import sys
import threading
import Interface as inter
import time
from Service import Service



class Display(Service):


    def init_config(self, service_conf):
        """
        Attributes:
            - state: dictonary
                most up to date state of the robots
            - comms: Comms
                Message queue manager
                Set up producer to server IP on port 3000
                Set up consumer on port 3100 to accept sensor data
            - g: Interface
                the GUI
            - config: dict
                config information about the swarm
        """
        
        self.g = inter.Interface()

        # wait for the user to pick a file
        while (len(self.g.get_config()) == 0):
            self.g.refresh_gui()

        self.config = self.g.get_config()

        # Connect to robots
        for item in self.config['mlist']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['ip'])
            self.state[item['ip']] = dict()
            for key in item['data'].keys():
                self.state[item['ip']][key] = 0

        # Connect to analytics
        self.active_analytics = []
        for item in self.config['alist']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['name'])
            self.active_analytics.append(item['name'])

        time.sleep(0.5)

    def reload(self):
        """
        dumps the subscribers and state and then goes through and re checks the config 
        """
        self.config = self.g.get_config()
        del self.comms
        self.comms = Comms()
        self.state.clear()

        for item in self.config['mlist']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['ip'])
            self.state[item['ip']] = dict()
            for key in item['data'].keys():
                self.state[item['ip']][key] = 0

        # Connect to analytics
        self.active_analytics = []
        for item in self.config['alist']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['name'])
            self.active_analytics.append(item['name'])

        time.sleep(0.5)

    def update_options(self):
        """
        Placeholder for when dispatcher becomes a thing
        """
        pass

    def transform(self):
        """
        used to listen for messages from the subscribers and update the internal state dictonary with new data when new messages are received
        """
        # Display applies no transformations and publishes nothing
        # Check for new messages over every analytic manually
        if "Status" in self.active_analytics:
            msg_status = self.comms.get("Status")
            if msg_status is not None:
                self.state[msg_status.topic]["Status"] = msg_status.payload["Status"]

        for ip in self.state.keys():
            # Check status data
            msg_recv = self.comms.get(ip)
            if msg_recv is not None:
                for key in msg_recv.payload.keys():
                    self.state[ip][key] = msg_recv.payload[key]
        return None

    def run(self):
        """
        indefinitely checks for new messages and updates the GUI with the current status of the robots
        Updates to GUI are sent even if no messages have been recieved since the last update
        """
        while True:

            # update state and transform data
            try:
                self.transform()
            except KeyError:
                pass

            # Prepare states for GUI
            bot_list = list()
            for ip in self.state.keys():
                ret_state = dict()
                ret_state[ip] = dict()
                for key in self.state[ip].keys():
                    #ret_state[ip][key] = key + " : " + str(self.state[ip][key])
                    ret_state[ip][key] = str(self.state[ip][key])
                bot_list.append(ret_state)

            # Update GUI
            self.g.refresh_gui()
            for bot in bot_list:
                self.g.update_display(bot)

             # Refresh Display if GUI has reloadd
            if self.g.get_reload() == True:
                self.reload()
                self.g.inform_reload()



if __name__ == "__main__":
    display = Display(sys.argv[1])
    display.run()