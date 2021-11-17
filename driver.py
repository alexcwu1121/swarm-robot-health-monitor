"""
driver.py:  Driver for SRHMD.
TODOS:      Depends on what other things we will implement.
Description:This file will mainly be responsive for calling out GUI for now.
"""

from Display import Display
import multiprocessing as mp
import sys
import os
import json

#sets up and runs a service
#type: the type of service that worker is running
#service_config: the configuration of the service being run
def worker(type, service_config):
    if type == 'Display':
        display = Display(service_config)
        display.run()
    else:
        print("No such service")

#launches all the services need for the application
def main():
    # launch services
    procs = []
    try:
        p = mp.Process(target=worker, args=('Display', None))
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
