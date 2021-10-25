"""
Srhmd.py
Daemon running on robot hosts that:
    - Extracts extrinsic data and keeps state
    - Extracts intrinsic data and aggregates with extrinsic data
    - Sends aggregated message to server
"""

from comms import Comms, Message
import threading
import psutil
import time

class Srhmd:
    def __init__(self, name, pub_hostname='0.0.0.0', update_interval=0.01, agg_interval=0.01):
        """
        Attributes:
        - comms
            Set up producer to server IP on port 3000. Needs to be configurable
                TODO: Don't hardcode exposed port on server
            Set up consumer on port 3100 to accept sensor data
        - ext_states
            dictionary holding extrinsic data states
        """
        self.name = name
        self.comms = Comms()
        self.comms.add_publisher_port(pub_hostname, '3000', self.name)
        self.comms.add_subscriber_port('127.0.0.1', '3100', 'ext_sensors')

        self.ext_sensors = dict()
        self.update_interval = update_interval
        self.agg_interval = agg_interval

    def update_ext(self):
        """
        Threaded
        Poll consumer for new sensor states and update ext_states
        :return:
            None
        """
        while True:
            # Poll all messages in buffer and substitute into ext_sensors
            msg = self.comms.get('ext_sensors')
            if msg is not None:
                key = next(iter(msg.payload))
                self.ext_sensors[key] = msg.payload.get(key)
                time.sleep(self.update_interval)

    def aggregator(self):
        """
        Threaded
        Extract intrinsic data and aggregate with ext_states
        Assemble message and publish to server
        :return:
            None
        """
        while True:
            # Payload dictionary
            payload = dict()

            # Core speed
            payload["cpu_freq"] = psutil.cpu_freq().current

            # Cpu usage
            for count, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                payload["cpu_percent" + str(count)] = percentage
            payload["cpu_percent"] = psutil.cpu_percent()

            # Memory usage
            svmem = psutil.virtual_memory()
            payload["svmem_total"] = svmem.total
            payload["svmem_available"] = svmem.available
            payload["svmem_used"] = svmem.used
            payload["svmem_percentage"] = svmem.percent

            # Aggregate with external sensors
            payload.update(self.ext_sensors)

            # Send payload
            print(payload)
            self.comms.send(self.name, Message(self.name, payload))

            # Refresh rate
            time.sleep(self.agg_interval)

    def run(self):
        """
        Start update_ext and aggregator threads
        :return:
            None
        """
        threads = []
        t = threading.Thread(target=self.update_ext)
        threads.append(t)
        t = threading.Thread(target=self.aggregator)
        threads.append(t)

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    srhmd = Srhmd("test1")
    srhmd.run()