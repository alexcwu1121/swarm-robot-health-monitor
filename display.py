from comms import Comms, Message
from datetime import datetime
from datetime import time
import json
import multiprocessing as mp
import os
import random
import sys
import time


class display_base:
    def __init__(self, fileN):
        self.comms = Comms()
        m_list = json.loads(open(fileN).read())
        
        portN = 4000
        
        for item in m_list['mlist']:
            print(item)
            self.comms.add_subscriber_port(item['ip'],str(portN),item['name'])


if __name__ == "__main__":
    my_rec = display_base(sys.argv[1])
    