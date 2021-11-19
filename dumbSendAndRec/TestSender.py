from Comms import Comms, Message
from datetime import datetime
from datetime import time
import multiprocessing as mp
import os
import random
import sys
import string
import time


class TestSender:
    def __init__(self):
        self.comms = Comms()
        #gets all the port names and numbers
        if(len(sys.argv) >= 2):
            for line in open(sys.argv[1]).readlines():
                if line == 'messages:\n':
                    break;
                if not(line == 'port_topic:\n'):
                    self.comms.add_publisher_port(line.split(',')[2].replace('\n',''),line.split(',')[1],line.split(',')[0])
        self.comms.add_publisher_port('127.0.0.1','3001','testInput')
        time.sleep(.1)
    
    def run(self):
        if(len(sys.argv) >= 2):
            time.sleep(.2)
            lines = open(sys.argv[1]).readlines()
            mess_place = 0
            for line in lines:
                mess_place+=1
                if line == 'messages:\n':
                    break
            lines = lines[mess_place::]
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
            to_send = input("enter a message to send or just press enter for a random message\n")
            if(to_send==''):
                for i in range(0,random.randint(1,128)):
                    to_send = to_send+random.choice(string.ascii_lowercase+string.ascii_uppercase)
            print(to_send)
            msg = Message('testInput', {1: to_send})
            self.comms.send('testInput', msg)
            time.sleep(.1)
        print("All done sending")
        exit()


if __name__ == "__main__":
    random.seed(datetime.now())

    my_sender = TestSender()
    
    my_sender.run()