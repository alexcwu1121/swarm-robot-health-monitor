from StatusAnalytic import StatusAnalytic
from ThresholdAnalytic import ThresholdAnalytic
from TimeoutAnalytic import TimeoutAnalytic
from comms import Comms
import multiprocessing as mp


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


if __name__ == "__main__":
    procs = []
    try:
        p = mp.Process(target=worker, args=('ThresholdAnalytic', None))
        procs.append(p)
        p.start()

        p = mp.Process(target=worker, args=('StatusAnalytic', None))
        procs.append(p)
        p.start()

        p = mp.Process(target=worker, args=('TimeoutAnalytic', None))
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
    print("here")
    sendOut = Comms()
    sendOut.add_publisher_port('127.0.0.1','3000','127.0.0.1')
    sendOut.send('127.0.0.1',{"cpu_freq":455})
