"""
driver.py:  Driver for SRHMD.
TODOS:      Depends on what other things we will implement.
Description:This file will mainly be responsive for calling out GUI for now.
"""

from Display import Display
from Interface import Interface
from StatusAnalytic import StatusAnalytic
from ThresholdAnalytic import ThresholdAnalytic
from TimeoutAnalytic import TimeoutAnalytic
import multiprocessing as mp
import sys
import os

#sets up and runs a service
#type: the type of service that worker is running
#service_config: the configuration of the service being run
def worker(type, service_config):
    if type == 'Display':
        display = Display(service_config)
        display.run()
    elif type == 'ThresholdAnalytic':
        threshold = ThresholdAnalytic(service_config)
        threshold.run()
    elif type == 'StatusAnalytic':
        status = StatusAnalytic(service_config)
        status.run()
    elif type == 'TimeoutAnalytic':
        timeout = TimeoutAnalytic(service_config)
        timeout.run()
    else:
        print("No such service")

#launches all the services need for the application
def main():
    g = Interface()
    while (len(g.get_config()) == 0):
       g.refresh_gui()
    config = g.get_config()
    # launch services
    procs = []
    try:
        p = mp.Process(target=worker, args=['Display', config])
        procs.append(p)
        p.start()

        p = mp.Process(target=worker, args=['ThresholdAnalytic', config])
        procs.append(p)
        p.start()

        p = mp.Process(target=worker, args=['StatusAnalytic', config])
        procs.append(p)
        p.start()

        p = mp.Process(target=worker, args=['TimeoutAnalytic', config])
        procs.append(p)
        p.start()

    except KeyboardInterrupt:
        print('Interrupted')
        for proc in procs:
            proc.terminate()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    
    while(True):
        # Update GUI
        g.refresh_gui()#REFACTOR
        for bot in bot_list:
            self.g.update_display(bot)#REFACTOR

        # Refresh Display if GUI has reload
        if self.g.get_reload() == True:#REFACTOR
            self.reload()
            self.g.inform_reload()#REFACTOR

if __name__ == "__main__":
    main()
