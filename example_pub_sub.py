"""example_pub_sub
    Start example publisher and subscriber processes
"""
from comms import Comms, Message
from datetime import time
import multiprocessing as mp
import time
import sys
import os

class pub_100:
    # Produce 100 integers from 0 to 99 in tenth second intervals
    def __init__(self):
        self.comms = Comms()
        self.comms.add_publisher_port('127.0.0.1','3001','integer')
        time.sleep(.1)

    def run(self):
        for i in range(100):
            msg = Message('integer', str(i))
            self.comms.send('integer', msg)
            #print(msg)
            time.sleep(.1)
        print("All done sending")
        exit()

class sub_100:
    # Consume integers using Comm's default get(), returning oldest message in queue
    # No message loss, but runs risk of missing backlogging lots of messages
    def __init__(self):
        self.comms = Comms()
        self.comms.add_subscriber_port('127.0.0.1','3001','integer')
        time.sleep(.1)

    def run(self):
        while True:
            msg_recv = self.comms.get('integer')
            if msg_recv is not None:
                print(msg_recv.payload)
                if msg_recv.payload == '99':
                    break
        print("All done receiving")
        exit()

class sub_100_clear:
    # Consume integers using Comm's get_clear(), returning the newest message and popping everything else
    # Always gets most recent message at the cost of intentional message dropping
    def __init__(self):
        self.comms = Comms()
        self.comms.add_subscriber_port('127.0.0.1','3001','integer')
        time.sleep(.1)

    def run(self):
        while True:
            time.sleep(0.5)
            msg_recv = self.comms.get_clear('integer')
            if msg_recv is not None:
                print(msg_recv.payload)
                if msg_recv.payload == '99':
                    break
        print("All done receiving")
        exit()

def worker(type):
    if type == 'pub':
        pub = pub_100()
        pub.run()
    elif type == 'sub':
        sub = sub_100()
        sub.run()
    elif type == 'subclear':
        sub = sub_100_clear()
        sub.run()
    else:
        print("pub or sub only")

if __name__ == "__main__":
    procs = []
    try:
        p = mp.Process(target=worker, args=('subclear',))
        procs.append(p)
        p.start()

        #p = mp.Process(target=worker, args=('sub',))
        #procs.append(p)
        #p.start()

        p = mp.Process(target=worker, args=('pub',))
        procs.append(p)
        p.start()

    except KeyboardInterrupt:
        print('Interrupted')
        for proc in procs:
            proc.terminate()
            proc.join()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)