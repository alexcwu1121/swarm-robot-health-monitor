from comms import Comms, Message
from datetime import datetime
from datetime import time
import json
import multiprocessing as mp
import os
import random
import sys
import threading
import time


class display_base:
    def __init__(self, fileN):
        self.comms = Comms()
        m_list = json.loads(open(fileN).read())
        self.state = dict()
        port_number = 4000
        
        for item in m_list['mlist']:
            self.comms.add_subscriber_port(item['ip'],item['port'],item['ip'])
            self.state[item['ip']] = dict()
            for key in item['data'].keys():
                self.state[item['ip']][key] = 0

    def keep_state(self,ip):
        while True:
            msg_recv = self.comms.get(ip)
            if msg_recv is not None:
                for key in msg_recv.payload.keys():
                    self.state[ip][key] = [msg_recv.payload[key]]

    def run_display(self):
        rec_threads = list()
        for ip in self.state.keys():
            rec_threads.append(threading.Thread(target=self.keep_state,args=(ip,)))
        for thr in rec_threads:
            thr.start()
        for thr in rec_threads:
            thr.join()

    def get_state(self):
        ret_ip = list(self.state)[0]
        ret_state = dict()
        ret_state[ret_ip] = dict()
        for key in self.state[ret_ip].keys():
            ret_state[ret_ip][key] = key + " : " + str(self.state[ret_ip][key])
        return ret_state


if __name__ == "__main__":
    my_rec = display_base(sys.argv[1])
    my_rec.run_display()