from StatusAnalytic import StatusAnalytic
from ThresholdAnalytic import ThresholdAnalytic
from TimeoutAnalytic import TimeoutAnalytic
from comms import Comms

if __name__ == "__main__":
    myTh = ThresholdAnalytic(None)
    myTi = TimeoutAnalytic(None)
    mySt = StatusAnalytic(None)
    myTh.run()
    myTi.run()
    mySt.run()
    sendOut = Comms()
    sendOut.add_publisher_port('127.0.0.1','3000','127.0.0.1')
    sendOut.send('127.0.0.1',{"cpu_freq":455})
