"""
driver.py:  Driver for SRHMD.
TODOS:      Depends on what other things we will implement.
Description:This file will mainly be responsive for calling out GUI for now.
"""

from Display import Display
from StatusAnalytic import StatusAnalytic
from ThresholdAnalytic import ThresholdAnalytic
from TimeoutAnalytic import TimeoutAnalytic
from Ingress import Ingress
import multiprocessing as mp
import sys
import os

"""
Initiates, sets up, and runs a service
Attributes:
    type: String
        The type of service that the worker is running
    service_config: Service
        The configuration of the service being run
Return:
    None
"""
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
    elif type == 'Ingress':
        ingress = Ingress(service_config)
        ingress.run()
    else:
        print("No such service")

"""
Launches all of the services needed to run the application
Return:
    None
"""
def main():
    # launch services
    procs = []
    try:
        p = mp.Process(target=worker, args=('Display', None))
        procs.append(p)
        p.start()

        p = mp.Process(target=worker, args=('ThresholdAnalytic', None))
        procs.append(p)
        p.start()

        p = mp.Process(target=worker, args=('StatusAnalytic', None))
        procs.append(p)
        p.start()

        p = mp.Process(target=worker, args=('TimeoutAnalytic', None))
        procs.append(p)
        p.start()

        p = mp.Process(target=worker, args=('Ingress', None))
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
