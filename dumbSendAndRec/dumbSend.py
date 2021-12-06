
"""
Dumb sender is designed to test the basic sending functionality of the zmq system
"""

from comms import Comms, Message
from datetime import time
import multiprocessing as mp
import time
import sys
import os
import random
from datetime import datetime
import string

class testSender:

	"""
        Inititates the communications for the test sender and establish
        a connection to port 3001 by default
        Return:
            None
    """
	def __init__(self):
		self.comms = Comms()
		self.comms.add_publisher_port('127.0.0.1','3001','testInput')
		time.sleep(.1)
	
	"""
        Parses system arguments for setup configuration, then loops and waits for messages.
		Each message is then sent as a test to the receiver, and a status is displayed
        Return:
            None
    """
	def run(self):
		if(len(sys.argv) >= 2):
			time.sleep(.2)
			lines = open(sys.argv[1]).readlines()
			
			
			for line in lines:
				parts = (line.replace("\n","").split(","))
				topic = parts[0]
				parts = parts[1::]
				contents = dict()
				for count in range(0,len(parts),2):
					contents[parts[count]] = parts[count+1]
				print(contents)
				print(topic)
				msg = Message(topic, contents)
				self.comms.send(topic, msg)
		
			exit()
	
		while True:
			toSend = input("enter a message to send or just press enter for a random message or DONE to turn of the reciever\n")
			if(toSend==''):
				for i in range(0,random.randint(1,128)):
					toSend = toSend+random.choice(string.ascii_lowercase+string.ascii_uppercase)
			print(toSend)
			msg = Message('testInput', {1: toSend})
			self.comms.send('testInput', msg)
			time.sleep(.1)
		print("All done sending")
		exit()
	
if __name__ == "__main__":

	random.seed(datetime.now())

	mySender = testSender()
	
	mySender.run()