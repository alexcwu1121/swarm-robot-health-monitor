"""
Aggregator.py
Collects and aggregates all of the data from all running services and sent it to Interface
    - creates a subscriber for every service
    - tracks the latest updates from the every service
    - maintains an internal dictonary that is updated whenever a new message sent from the service
    - updates self when Interface updates
    - sends updates from Interface to Dispatch
"""

from comms import Comms
from comms import Message
import json
import sys
from Interface import Interface
import time
from Service import Service

class Dispatcher(Service):

    def __init__(self):
        """
        Attributes:
            - g: Interface
                the GUI
            - services: dictonary
                list of services
            - comms: Comms
                Message queue manager
                Set up producer to Dispatcher with config IP and port
                Set up consumer on all Services with config IP and port
            - state: dict
                collection of all Services datas with robot IP as key
        """

        #Initialize the attributes
        self.comms = Comms()
        self.config = {}

        #Open service_config and subscribes to all Services and publish to Dispatcher
        #Also keep tracks the Services subscribed
        #If there is a problem with service_config.json print error and exit unsuccessfully
        try:
            with open("config/service_config.json") as f:
                config = json.load(f)
                self.comms.add_publisher_port(config["Dispatcher"]["ip"],
                                                config["Dispatcher"]["port"],
                                                "Dispatcher")
                self.comms.add_subscriber_port(config["Aggregator"]['ip'],
                                                config["Aggregator"]['port'], 
                                                "Aggregator")
        except:
            print("Service Config error!")
            exit(1)

        time.sleep(0.5)

    def set_config(self, config):
        '''
        Updates the current state attribute with given a config then 
        Publishes the given config from interface to Dispatch
        '''
        self.config = config
        self.comms.send("Dispatcher", Message("Config", config))
        time.sleep(0.5)
        
    def transform(self):
        return super().transform()
    # def update_options(self):
    #     """
    #     Placeholder for when dispatcher becomes a thing
    #     """
    #     pass

    # def transform(self):
    #     """
    #     used to listen for messages from the subscribers and update the internal state dictonary with new data when new messages are received
    #     """
    #     # Check for new message from all sevices and update internal state
    #     for sub in list(self.services.keys()):
    #         msg = self.comms.get(sub)
    #         if msg is not None:
    #             if msg.topic in list(self.state.keys()):
    #                 self.state[msg.topic].update(msg.payload)
    #             else:
    #                 self.state[msg.topic] = msg.payload
    #     return None

    def run(self):
        """
        indefinitely checks for new messages and updates the GUI with the current status of the robots
        Updates to GUI are sent even if no messages have been recieved since the last update
        """
        while True:
            # update state and transform data
            # try:
            #     self.transform()
            # except KeyError:
            #     pass

            # Prepare states for GUI
            # robot_list = list()
            # for ip in self.state.keys():
            #     ret_state = dict()
            #     ret_state[ip] = dict()
            #     for key in self.state[ip].keys():
            #         #ret_state[ip][key] = key + " : " + str(self.state[ip][key])
            #         ret_state[ip][key] = str(self.state[ip][key])
            #     robot_list.append(ret_state)

            # Update GUI
            # self.g.refresh_gui()
            # for bot in robot_list:
            #     self.g.update_display(bot)

            # Update Display if GUI has reload and send new config to Dispatch
            try:
                msg = self.comms.get("Aggregator")
                if msg is not None:
                    self.set_config(msg.payload)
            except KeyError:
                pass



if __name__ == "__main__":
    a = Dispatcher(sys.argv[1])
    a.run()