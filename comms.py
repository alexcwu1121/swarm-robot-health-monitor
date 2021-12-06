""" 
Comms Message queue manager's purpose is to facilitate the creation and management of connections 
"""
import zmq
import pickle
import logging

LOG = logging.getLogger("comms")
LOG.setLevel(level=logging.INFO)

#Comms' purpose is to create and manage zmq connections in an easier to use way than using zmq directly
class Comms:
    
    """
        Initiates publisher ports, subscriber ports, and subscriber queues
        Return:
            None
    """
    def __init__(self):
        self.subscriber_ports = {}
        self.publisher_ports = {}

    """
        Create a zmq publisher port
        Arguments:
            ip: String
                The ip address of the new publisher port
            port: int
                The port number of the new publisher port
            topic: String
                The topic name of the new publisher port
        Return:
            None
    """
    def add_publisher_port(self, ip, port, topic):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://{}:{}".format(ip, port))
        self.publisher_ports[topic] = socket

    """
        Create a zmq subscriber port
        Arguments:
            ip: String
                The ip address of the new publisher port
            port: int
                The port number of the new publisher port
            topic: String
                The topic name of the new publisher port
        Return: None
    """
    def add_subscriber_port(self, ip, port, topic):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.setsockopt_string(zmq.SUBSCRIBE, "")
        socket.setsockopt(zmq.CONFLATE, 1)
        socket.connect("tcp://{}:{}".format(ip, port))
        self.subscriber_ports[topic] = socket

    """
        Get the top message sent to a given topic and remove it from the
        subscriber queue
        Arguments:
            topic: String
                The topic to get the message from 
        Return: 
            None
    """
    def get(self, topic):
        try:
            return pickle.loads(self.subscriber_ports[topic].recv(flags=zmq.NOBLOCK))
        except zmq.Again:
            pass

   """
        Send a message using a publisher port
        Arguments:
            topic: String
                The topic to send the message to
            message: String
                The message to be sent to the topic
        Return: 
            None
    """
    def send(self, topic, message):
        encoded = pickle.dumps(message)
        self.publisher_ports[topic].send(encoded)


""" This class is sent between publishers and subscribers """
class Message:
    """
        Set up the message class
        Arguments:
            payload: Dict()
                The content of the message being sent 
        Return:
            None
    """
    def __init__(self, topic, payload):
        self.topic = topic
        self.payload = payload

    """
        Converts a message object into a string
        Return:
            A string representation of the message
    """
    def __str__(self):
        return(">"*20+"\nTopic: {}\nPayload: \n{}\n"
               .format(self.topic,self.payload)+">"*20)
