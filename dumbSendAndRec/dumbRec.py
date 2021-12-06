"""
Dumb receiver is designed to test the basic receiving functionality of the zmq system
"""

from comms import Comms, Message
from datetime import time
import multiprocessing as mp
import time
import sys
import os
import random
from datetime import datetime


class testReciever:

	"""
        Inititates the communications for the test receiver and establish
        a connection to port 3001 by default
        Return:
            None
    """
	def __init__(self):
		self.comms = Comms()
		self.comms.add_subscriber_port('127.0.0.1','3001','testInput')
		time.sleep(.1)

	"""
        Runs a test of the receiver and prints the status
        Return:
            None
    """
	def run(self):
		while True:
			msg_recv = self.comms.get('testInput')
			if msg_recv is not None:
				print(msg_recv.payload)
		print("All done receiving")
		exit()
	


if __name__ == "__main__":
	random.seed(datetime.now())
	
	myRec = testReciever()
	
	myRec.run()
	