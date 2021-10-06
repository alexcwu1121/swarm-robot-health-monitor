"""
Srhmd.py
Daemon running on robot hosts that:
    - Extracts extrinsic data and keeps state
    - Extracts intrinsic data and aggregates with extrinsic data
    - Sends aggregated message to server
"""
class Srhmd:
    def __init__(self, server_hostname):
        """
        Attributes:
        - comms
            Set up producer to server IP. Needs to be configurable
            Set up consumer on port 3100 to accept sensor data
        - ext_states
            dictionary holding extrinsic data states
        """
        pass

    def update_ext(self):
        """
        Threaded
        Poll consumer for new sensor states and update ext_states
        :return:
            None
        """
        pass

    def aggregator(self):
        """
        Threaded
        Extract intrinsic data and aggregate with ext_states
        Assemble message and publish to server
        :return:
            None
        """
        pass

    def run(self):
        """
        Start update_ext and aggregator threads
        :return:
            None
        """
        pass

if __name__ == "__main__":
    srhmd = Srhmd("localhost")
    srhmd.run()