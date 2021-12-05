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

        # Connect to analytics
        for item in self.config['alist']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['name'])

        time.sleep(0.5)

    def reload(self):
        """
        dumps the subscribers and state and then goes through and re checks the config 
        """
        self.config = self.g.get_config()
        del self.comms
        self.comms = Comms()
        self.state.clear()

        # Connect to analytics
        for item in self.config['alist']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['name'])

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
        for topic in self.comms.subscriber_ports.keys():
            msg_recv = self.comms.get(topic)
            if msg_recv is not None:
                if msg_recv.topic in self.state.keys():
                    self.state[msg_recv.topic].update(msg_recv.payload)
                else:
                    self.state[msg_recv.topic] = msg_recv.payload
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