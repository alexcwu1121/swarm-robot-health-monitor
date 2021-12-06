"""
driver.py:  Driver for SRHMD.
TODOS:      Depends on what other things we will implement.
Description:This file will mainly be responsive for calling out GUI for now.
"""

from Aggregator import Aggregator
from Dispatcher import Dispatcher
from StatusAnalytic import StatusAnalytic
from ThresholdAnalytic import ThresholdAnalytic
from TimeoutAnalytic import TimeoutAnalytic
from Ingress import Ingress
import multiprocessing as mp
import sys
import os

#sets up and runs a service
#type: the type of service that worker is running
#service_config: the configuration of the service being run
def worker(type):
    if type == 'Aggregator':
        aggregator = Aggregator()
        aggregator.run()
    elif type == 'Dispatcher':
        dispatcher = Dispatcher()
        dispatcher.run()
    elif type == 'Ingress':
        ingress = Ingress()
        ingress.run()
    elif type == 'ThresholdAnalytic':
        threshold = ThresholdAnalytic()
        threshold.run()
    elif type == 'TimeoutAnalytic':
        timeout = TimeoutAnalytic()
        timeout.run()
    elif type == 'StatusAnalytic':
        status = StatusAnalytic()
        status.run()
    else:
        print("No such service")

#launches all the services need for the application
def main():
    # launch services
    procs = []
    try:
        p = mp.Process(target=worker, args=['Aggregator'])
        procs.append(p)
        p.start()

        p = mp.Process(target=worker, args=['Ingress'])
        procs.append(p)
        p.start()

        p = mp.Process(target=worker, args=['ThresholdAnalytic'])
        procs.append(p)
        p.start()

        p = mp.Process(target=worker, args=['TimeoutAnalytic'])
        procs.append(p)
        p.start()

        p = mp.Process(target=worker, args=['StatusAnalytic'])
        procs.append(p)
        p.start()

        p = mp.Process(target=worker, args=['Dispatcher'])
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
    

if __name__ == "__main__":
    main()
