from comms import Comms, Message
from datetime import time
import multiprocessing as mp
import time
import sys
import os
import random
from datetime import datetime



	
	
class testReciever:
	def __init__(self):
		self.comms = Comms()
		self.comms.add_subscriber_port('127.0.0.1','3001','testInput')
		time.sleep(.1)

	def run(self):
		while True:
			msg_recv = self.comms.get('testInput')
			if msg_recv is not None:
				print(msg_recv.payload[1])
				if msg_recv.payload[1] == 'DONE':
					break
		print("All done receiving")
		exit()
	


if __name__ == "__main__":
	random.seed(datetime.now())
	
	myRec = testReciever()
	
	myRec.run()
	