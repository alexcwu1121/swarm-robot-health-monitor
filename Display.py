from comms import Comms
import json
import sys
import threading
import interface as inter
import time
from Service import Service

#Display's purpose is to manage the server's connections to all the robots in the swarm
#Display does this by creating a subscriber for every robot in the swarm and then keep tracking of the latest updates from these robots
#these updates are kept track of through an internal dictonary that is updated whenever a new message is sent to the server from a robot
#containing more up to date information
class Display(Service):

    #init_config sets up the subscribers
    #server_conf: currently unused
    def init_config(self, service_conf):
        self.g = inter.Gui()

        # wait for the user to pick a file
        while (self.g.get_config() == ''):
            self.g.refresh_gui()

        self.config = json.loads(open(self.g.get_config()).read())

        for item in self.config['mlist']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['ip'])
            self.state[item['ip']] = dict()
            for key in item['data'].keys():
                self.state[item['ip']][key] = 0
        time.sleep(0.5)

    #(will be) used to add or remove subscribers when the user adds or removes robots
    def update_options(self):
        # Placeholder for when dispatcher becomes a thing
        pass

    #used to listen for messages from the subscribers and update the internal state dictonary with new data when new messages are received
    def transform(self):
        # Display applies no transformations and publishes nothing
        for ip in self.state.keys():
            msg_recv = self.comms.get(ip)
            if msg_recv is not None:
                for key in msg_recv.payload.keys():
                    self.state[ip][key] = [msg_recv.payload[key]]
        return None

    #indefinitely checks for new messages and updates the GUI with the current status of the robots
    #Updates to GUI are sent even if no messages have been recieved since the last update
    def run(self):
        while True:
            # update state and transform data
            self.transform()

            # Prepare states for GUI
            bot_list = list()
            for ip in self.state.keys():
                ret_state = dict()
                ret_state[ip] = dict()
                for key in self.state[ip].keys():
                    ret_state[ip][key] = key + " : " + str(self.state[ip][key])
                bot_list.append(ret_state)

            # Update GUI
            self.g.refresh_gui()
            for bot in bot_list:
                self.g.update_display(bot)


if __name__ == "__main__":
    display = Display(sys.argv[1])
    display.run()