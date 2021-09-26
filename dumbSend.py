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
	def __init__(self):
		self.comms = Comms()
		self.comms.add_publisher_port('127.0.0.1','3001','testInput')
		time.sleep(.1)
	
	def run(self):
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