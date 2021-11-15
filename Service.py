from abc import ABC, abstractmethod
from comms import Comms
import json
import sys
import time
import threading

class Service(ABC):
    def __init__(self, service_conf):
        self.config = dict()
        self.state = dict()
        self.comms = Comms()

        self.init_config(service_conf)

    @abstractmethod
    def init_config(self):
        pass

    @abstractmethod
    def update_options(self):
        pass

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def run(self):
        pass