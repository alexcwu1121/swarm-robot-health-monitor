from comms import Comms
import json
import sys
import threading
import interface as inter
import time
from Service import Service


class Display(Service):

    def init_config(self, service_conf):
        self.g = inter.Gui()

        # wait for the user to pick a file
        while (len(self.g.get_config()) == 0):
            self.g.refresh_gui()

        self.config = self.g.get_config()

        for item in self.config['mlist']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['ip'])
            self.state[item['ip']] = dict()
            for key in item['data'].keys():
                self.state[item['ip']][key] = 0
        time.sleep(0.5)

    def relode(self):
        self.config = self.g.get_config()
        del self.comms
        self.comms = Comms()
        self.state.clear()

        for item in self.config['mlist']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['ip'])
            self.state[item['ip']] = dict()
            for key in item['data'].keys():
                self.state[item['ip']][key] = 0
        time.sleep(0.5)

    def update_options(self):
        # Placeholder for when dispatcher becomes a thing
        pass

    def transform(self):
        # Display applies no transformations and publishes nothing
        for ip in self.state.keys():
            msg_recv = self.comms.get(ip)
            if msg_recv is not None:
                for key in msg_recv.payload.keys():
                    self.state[ip][key] = [msg_recv.payload[key]]
        return None

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

            # Refresh Display if GUI has reloded
            if self.g.get_relode() == True:
                self.relode()
                self.g.inform_reloded()



if __name__ == "__main__":
    display = Display(sys.argv[1])
    display.run()