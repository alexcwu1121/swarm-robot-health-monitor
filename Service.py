"""
Service.py:  Base class for server analytics
Description: Base class for server analytics
"""

from abc import ABC, abstractmethod
from comms import Comms

class Service(ABC):
    @abstractmethod
    def __init__(self):
        """Initialize self and wait for config"""
        pass

    @abstractmethod
    def set_config(self):
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