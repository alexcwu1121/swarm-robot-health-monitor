import sys
import json
import time
from Service import Service
from Comms import Message

class StatusAnalytic(Service):

    def init_config(self, service_conf):
        # TODO: don't hardcode this config file. get it from gui
        with open("config/config_status.json") as f:
            self.analytic_config = json.load(f)

        self.status_conditions = self.analytic_config['Status']['conditions']

        # Set up subscribers according to config
        for item in self.analytic_config['Status']['subscribe']:
            self.comms.add_subscriber_port(item['ip'], item['port'], item['topic'])

        # Set up publisher according to config
        ip = self.analytic_config['Status']['publish']['ip']
        port = self.analytic_config['Status']['publish']['port']
        self.comms.add_publisher_port(ip, port, 'Status')

        time.sleep(0.5)

    def update_options(self):
        pass

    def transform(self):
        msg_recv = self.comms.get('Threshold')
        if msg_recv is not None:

            if msg_recv.topic not in self.state.keys():
                self.state[msg_recv.topic] = {}

            for key in msg_recv.payload.keys():
                self.state[msg_recv.topic][key] = msg_recv.payload[key]
        return

    def get_status(self, state):
        status = {}

        values = list(state.values())
        failures = len(values) - sum([value for value in values])
        #print(failures)

        if failures <= int(self.status_conditions["nominal"]):
            status["Status"] = "nominal"
        elif failures <= int(self.status_conditions["warning"]):
            status["Status"] = "warning"
        else:
            status["Status"] = "critical"
        return status

    def run(self):
        while True:
            # update state and transform data
            self.transform()

            for ip in self.state.keys():
                status = self.get_status(self.state[ip])
                self.comms.send("Status", Message(ip, status))


if __name__ == "__main__":
    status = StatusAnalytic()
    status.run()