"""
BlackBoxTests.py used to run black box tests on services
to run the threshold tests run python BlackBoxTests.py Threshold
to run the status tests run python BlackBoxTests.py Status
"""
from StatusAnalytic import StatusAnalytic
from ThresholdAnalytic import ThresholdAnalytic
from TimeoutAnalytic import TimeoutAnalytic
from comms import Comms
from comms import Message
import multiprocessing as mp
import time
import sys

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
"""
Topic: the topic to send the test message to
TestTopic: the topic of the value being sent in the message
TestVal: the value in the test message
Expected: the expcted value to get back
SubAndSend: the Comms object being used to communicate with the service
"""
def ThresholdServiceTest(Topic, TestTopic, TestVal, Expected, SubAndSend):
    SubAndSend.send(Topic,Message(Topic, {TestTopic:TestVal}))
    time.sleep(.1)
    val_back = SubAndSend.get(Topic).payload[TestTopic]
    print("test of " + TestTopic + " with value of " + str(TestVal) + " excepting " + str(Expected) + " got " + str(val_back))
    if(val_back == Expected):
        print("test passed")
    else:
        print("test failed")
    return val_back == Expected
"""
Topic: the topic to send the test message to
TestTopic: the topic of the value being sent in the message
TestVal: the value in the test message
Expected: the expcted value to get back
SubAndSend: the Comms object being used to communicate with the service
"""
def StatusServiceTest(Topic, TestTopic, TestVal, Expected, SubAndSend):
    SubAndSend.send(Topic,Message(Topic, {TestTopic:TestVal}))
    val_back = SendOutStatus.get("Status")
    while(val_back == None):
        val_back = SendOutStatus.get("Status")
    val_back = val_back.payload["Status"]
    print("test of " + TestTopic + " with value of " + str(TestVal) + " excepting " + str(Expected) + " got " + str(val_back))
    if(val_back == Expected):
        print("test passed")
    else:
        print("test failed")
    return val_back == Expected

if __name__ == "__main__":
    if(sys.argv[1] == "Threshold"):
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
        #threshold test
        SendOutThres = Comms()
        SendOutThres.add_publisher_port('127.0.0.1','4000','Ingress')
        SendOutThres.add_subscriber_port('127.0.0.1','2900','Ingress')
        time.sleep(.7)
        #over
        ThresholdServiceTest('Ingress',"svmem_percentage",45,False,SendOutThres)
        #in range
        ThresholdServiceTest('Ingress',"svmem_percentage",35,True,SendOutThres)
        #under
        ThresholdServiceTest('Ingress',"svmem_percentage",18,False,SendOutThres)
    if(sys.argv[1] == "Status"):
        procs = []
        try:
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
        #Status test
        SendOutStatus = Comms()
        SendOutStatus.add_publisher_port('127.0.0.1','2900','Threshold')
        SendOutStatus.add_subscriber_port('127.0.0.1','2902','Status')
        time.sleep(.7)
        StatusServiceTest("Threshold","Threshold",True,"nominal",SendOutStatus)
        StatusServiceTest("Threshold","Threshold",False,"nominal",SendOutStatus)
