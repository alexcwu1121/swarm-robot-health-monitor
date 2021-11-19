"""
Service.py:  Base class for server analytics
Description: Base class for server analytics
"""

from abc import ABC, abstractmethod
from Comms import Comms

class Service(ABC):
    def __init__(self, service_conf):
        """
        Attributes:
            - config: Dict<String:Float>
                Dictionaries of options
            - comms: Comms
                Message queue manager
            - state: Dict<String:Float>
                State of each ingressed data field
        """
        self.config = dict()
        self.state = dict()
        self.comms = Comms()

        self.init_config(service_conf)

    @abstractmethod
    def init_config(self):
        """Initialize options from a configuration file"""
        pass

    @abstractmethod
    def update_options(self):
        """Update options from dispatcher messages"""
        pass

    @abstractmethod
    def transform(self):
        """Transform a data stream and publish"""
        pass

    @abstractmethod
    def run(self):
        """Initialize, establish connections, and launch"""
        pass