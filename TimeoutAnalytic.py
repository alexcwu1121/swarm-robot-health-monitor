import sys
import json
import time
from Service import Service
from comms import Message

class TimeoutAnalytic(Service):

    def init_config(self, service_conf):
        # TODO: don't hardcode this config file. get it from gui
        with open("config/config_testing_c.json") as f:
            self.config = json.load(f)

        # TODO: don't hardcode this config file. get it from gui
        with open("config/config_timeout.json") as f:
            self.analytic_config = json.load(f)

        self.timeout = float(self.analytic_config['Timeout']['timeout'])

        # Connect to robots
        for item in self.config['mlist']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['ip'])
            self.state[item['ip']] = dict()
            self.state[item['ip']]["Timeout"] = 0
            self.state[item['ip']]["PrevTime"] = time.process_time()

        # Set up publisher according to config
        ip = self.analytic_config['Timeout']['publish']['ip']
        port = self.analytic_config['Timeout']['publish']['port']
        self.comms.add_publisher_port(ip, port, 'Timeout')

        time.sleep(0.5)

    def update_options(self):
        pass

    def transform(self):
        for ip in self.state.keys():
            msg_recv = self.comms.get(ip)
            if msg_recv is not None:
                self.state[msg_recv.topic]["PrevTime"] = time.process_time()
            self.state[ip]["Timeout"] = time.process_time() - self.state[ip]["PrevTime"]
        return

    def run(self):
        while True:
            # update state and transform data
            self.transform()

            for ip in self.state.keys():
                timeout = {"Timeout": True}
                if self.state[ip]["Timeout"] > self.timeout:
                    timeout["Timeout"] = False
                self.comms.send("Timeout", Message(ip, timeout))


if __name__ == "__main__":
    timeout = TimeoutAnalytic()
    timeout.run()