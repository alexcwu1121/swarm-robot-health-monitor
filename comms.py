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

#Comms' purpose is to create and manage zmq connections in an easier to use way than using zmq directly
class Comms:
    #initiates subscriber ports, publisher ports and subscriber queues
    def __init__(self):
        self.subscriber_ports = {}
        self.publisher_ports = {}
        self.subscriber_queues = {}

    #creats a zmq publisher port
    #ip: the ip address of the new publisher port
    #port: the port number of the new publisher port
    #topic: the topic of the new publisher port
    def add_publisher_port(self, ip, port, topic):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://{}:{}".format(ip, port))
        self.publisher_ports[topic] = socket

    #indefinitely checks for new messages for all open topics
    #if a message has been recieved then it is added to the subscriber queue for the topic the message was for
    def __receive(self, topic):
        while True:
            message = self.subscriber_ports[topic].recv()
            self.subscriber_queues[topic].put(message)
            time.sleep(.00000001)

    #creats a zmq subscriber port
    #ip: the ip address of the new subscriber port
    #port: the port number of the new subscriber port
    #topic: the topic of the new subscriber port
    def add_subscriber_port(self, ip, port, topic):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.setsockopt_string(zmq.SUBSCRIBE, "")
        socket.connect("tcp://{}:{}".format(ip, port))
        self.subscriber_ports[topic] = socket
        self.subscriber_queues[topic] = Queue()
        t = threading.Thread(target=self.__receive, args=(topic,))
        t.start()

    #gets the top message sent to a topic and removes it from the subscriber queue
    #topic: the topic to get the message from
    def get(self, topic):
        try:
            encoded = self.subscriber_queues[topic].get(False)
            return pickle.loads(encoded)
        except queue.Empty:
            return None
    
    #gets the most recent message sent to a topic and empties the subscriber queue
    #topic: the topic to get a message of and empty the queue of
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

    #sends a message using a publisher port
    #topic: the topic 
    def send(self, topic, message):
        encoded = pickle.dumps(message)
        self.publisher_ports[topic].send(encoded)


#the class that is sent between publishers and subscribers
class Message:
    #sets up the message class
    #topic: the topic to send the message to
    #payload: the content of the message being sent
    def __init__(self, topic, payload):
        # payload is a dictionary
        self.topic = topic
        self.payload = payload

    #converts a message object into a string
    def __str__(self):
        return(">"*20+"\nTopic: {}\nPayload: \n{}\n"
               .format(self.topic,self.payload)+">"*20)
