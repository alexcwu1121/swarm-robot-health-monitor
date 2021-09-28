"""example_pub_sub
    Start example publisher and subscriber processes
    Comms testing:

    Structured tests
    1. Add one subscriber socket
    2. Add one producer socket
    3. Add two subscriber sockets
    4. Add two producer sockets

    Unstructured tests
    Assume usage of Comms.get() whenever not specified
    5. Producer starts quickly sending immediately and consumer starts immediately
        -> consumer receives nothing (consumer socket takes time to set up)
    6. Producer waits 1 second, then sends messages at any rate and consumer receives at any rate
        -> consumer prints integers in sequence
    7. Producer waits 1 second, then sends messages faster than consumer calls get_clear()
        -> consumer skips messages
    8. Producer waits 5 seconds, then sends messages at any rate and consumer starts immediately
        -> consumer starts printing after 5s
    9. Producer starts slowly sending immediately while consumer waits 5s before start
        -> consumer quickly prints first messages, then prints the rest at producer rate

    Not tested
    10. Two producers send to one consumer
        -> ZMQ sockets only allow one producer per port on a single machine.
    11. One producer sends to two consumers
        -> ZMQ subbing to multiple ports not yet implemented
"""
from comms import Comms, Message
from datetime import time
import multiprocessing as mp
import time
import sys
import os
import unittest

class pub_100:
    # Produce 100 integers from 0 to 99 in tenth second intervals
    def __init__(self, init_delay, rep_delay, p_msg, port):
        self.comms = Comms()
        self.comms.add_publisher_port('127.0.0.1',port,'integer')

        self.init_delay = init_delay
        self.rep_delay = rep_delay
        self.p_msg = p_msg

    def run(self):
        time.sleep(self.init_delay)
        for i in range(100):
            msg = Message('integer', str(i))
            self.comms.send('integer', msg)

            if self.p_msg:
                print(msg)
            time.sleep(self.rep_delay)

        print("All done sending")
        exit()

class sub_100:
    # Consume integers using Comm's default get(), returning oldest message in queue
    # No message loss, but runs risk of missing backlogging lots of messages
    def __init__(self, init_delay, rep_delay, p_msg, get_c, port):
        self.comms = Comms()
        self.comms.add_subscriber_port('127.0.0.1',port,'integer')

        self.init_delay = init_delay
        self.rep_delay = rep_delay
        self.p_msg = p_msg
        self.get_c = get_c

    def run(self):
        time.sleep(self.init_delay)
        while True:
            msg_recv = None
            if self.get_c:
                msg_recv = self.comms.get_clear('integer')
            else:
                msg_recv = self.comms.get('integer')

            if msg_recv is not None:
                if self.p_msg:
                    print(msg_recv)
                if msg_recv.payload == '99':
                    break
            time.sleep(self.rep_delay)

        print("All done receiving")
        exit()

def worker(type, init_delay=0, rep_delay=0, p_msg=False, get_c=False, port=3001):
    if type == 'pub':
        pub = pub_100(init_delay, rep_delay, p_msg, port)
        pub.run()
    elif type == 'sub':
        sub = sub_100(init_delay, rep_delay, p_msg, get_c, port)
        sub.run()
    elif type == 'subclear':
        sub = sub_100_clear()
        sub.run()
    else:
        print("pub or sub only")

class TestCommsSetup(unittest.TestCase):
    def test_add_sub(self):
        comms = Comms()
        comms.add_subscriber_port('127.0.0.1', '3001', 'foo')
        self.assertTrue(len(comms.subscriber_ports.keys())==1)

    def test_add_prod(self):
        comms = Comms()
        comms.add_publisher_port('127.0.0.1', '3001', 'foo')
        self.assertTrue(len(comms.publisher_ports.keys()) == 1)

    def test_add_sub2(self):
        comms = Comms()
        comms.add_subscriber_port('127.0.0.1', '3001', 'foo')
        comms.add_subscriber_port('127.0.0.1', '3002', 'bar')
        self.assertTrue(len(comms.subscriber_ports.keys()) == 2)

    def test_add_prod2(self):
        comms = Comms()
        comms.add_publisher_port('127.0.0.1', '3001', 'foo')
        comms.add_publisher_port('127.0.0.1', '3002', 'bar')
        self.assertTrue(len(comms.publisher_ports.keys()) == 2)

if __name__ == "__main__":
    unittest.main()

    procs = []
    try:
        """
        # Case 5
        p = mp.Process(target=worker, args=('pub', 0, 0, False, False))
        procs.append(p)
        p.start()
        p = mp.Process(target=worker, args=('sub', 0, 0, True, False))
        procs.append(p)
        p.start()
        """

        """
        # Case 6
        p = mp.Process(target=worker, args=('pub', 1, 0, False, False))
        procs.append(p)
        p.start()
        p = mp.Process(target=worker, args=('sub', 0, 0, True, False))
        procs.append(p)
        p.start()
        """

        """
        # Case 7
        p = mp.Process(target=worker, args=('pub', 1, 0.2, False, False))
        procs.append(p)
        p.start()
        p = mp.Process(target=worker, args=('sub', 0, 0.5, True, True))
        procs.append(p)
        p.start()
        """

        """
        # Case 8
        p = mp.Process(target=worker, args=('pub', 5, 0, False, False))
        procs.append(p)
        p.start()
        p = mp.Process(target=worker, args=('sub', 0, 0, True, False))
        procs.append(p)
        p.start()
        """

        """
        # Case 9
        p = mp.Process(target=worker, args=('pub', 0, 0.5, False, False))
        procs.append(p)
        p.start()
        p = mp.Process(target=worker, args=('sub', 5, 0, True, False))
        procs.append(p)
        p.start()
        """

    except KeyboardInterrupt:
        print('Interrupted')
        for proc in procs:
            proc.terminate()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)