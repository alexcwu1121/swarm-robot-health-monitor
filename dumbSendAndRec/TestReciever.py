from Comms import Comms, Message
from datetime import datetime
from datetime import time
import multiprocessing as mp
import os
import random
import sys
import time


class TestReciever:
    
    def __init__(self):
        self.comms = Comms()
        self.ip_num = '127.0.0.1'
        self.port_num = '3001'
        self.topic_name = 'testInput'
        if len(sys.argv) == 4:
            self.ip_num = sys.argv[1]
            self.port_num = sys.argv[2]
            self.topic_name = sys.argv[3].replace('\n','')
        self.comms.add_subscriber_port(self.ip_num,self.port_num,self.topic_name)
        time.sleep(.1)

    def run(self):
        while True:
            msg_recv = self.comms.get(self.topic_name)
            if msg_recv is not None:
                print(msg_recv.payload)
        print("All done receiving")
        exit()


if __name__ == "__main__":
    random.seed(datetime.now())

    my_rec = TestReciever()

    my_rec.run()
    