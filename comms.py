""" Comms
    Message queue manager
"""
import zmq
from queue import *
import queue
import time
import threading
import pickle
import logging

LOG = logging.getLogger("comms")
LOG.setLevel(level=logging.INFO)

class Comms:
    def __init__(self):
        self.subscriber_ports = {}
        self.publisher_ports = {}
        self.subscriber_queues = {}

    def add_publisher_port(self, ip, port, topic):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://{}:{}".format(ip, port))
        self.publisher_ports[topic] = socket

    def __receive(self, topic):
        while True:
            message = self.subscriber_ports[topic].recv()
            self.subscriber_queues[topic].put(message)
            time.sleep(.00000001)

    def add_subscriber_port(self, ip, port, topic):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.setsockopt_string(zmq.SUBSCRIBE, "")
        socket.connect("tcp://{}:{}".format(ip, port))
        self.subscriber_ports[topic] = socket
        self.subscriber_queues[topic] = Queue()
        t = threading.Thread(target=self.__receive, args=(topic,))
        t.start()

    def get(self, topic):
        try:
            encoded = self.subscriber_queues[topic].get(False)
            return pickle.loads(encoded)
        except queue.Empty:
            return None

    def get_clear(self, topic):
        # Didn't just loop get() because deserialization
        encoded = None
        while True:
            try:
                encoded = self.subscriber_queues[topic].get(False)
            except queue.Empty:
                break
        if encoded is not None:
            return pickle.loads(encoded)
        return encoded

    def send(self, topic, message):
        encoded = pickle.dumps(message)
        self.publisher_ports[topic].send(encoded)


class Message:
    def __init__(self, topic, payload):
        # payload is a dictionary
        self.topic = topic
        self.payload = payload

    def __str__(self):
        return(">"*20+"\nTopic: {}\nPayload: \n{}\n"
               .format(self.topic,self.payload)+">"*20)
