""" Comms
    Message queue manager
"""
import zmq
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

    #creats a zmq publisher port
    #ip: the ip address of the new publisher port
    #port: the port number of the new publisher port
    #topic: the topic of the new publisher port
    def add_publisher_port(self, ip, port, topic):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://{}:{}".format(ip, port))
        self.publisher_ports[topic] = socket

    #creats a zmq subscriber port
    #ip: the ip address of the new subscriber port
    #port: the port number of the new subscriber port
    #topic: the topic of the new subscriber port
    def add_subscriber_port(self, ip, port, topic):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.setsockopt_string(zmq.SUBSCRIBE, "")
        socket.setsockopt(zmq.CONFLATE, 1)
        socket.connect("tcp://{}:{}".format(ip, port))
        self.subscriber_ports[topic] = socket

    #gets the top message sent to a topic and removes it from the subscriber queue
    #topic: the topic to get the message from
    def get(self, topic):
        try:
            return pickle.loads(self.subscriber_ports[topic].recv(flags=zmq.NOBLOCK))
        except zmq.Again:
            pass

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
