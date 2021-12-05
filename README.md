# swarm-robot-health-monitor
swarm-robot-health-monitor(SRHM) is an application used to monitor the resource use, health and sensor of robot swarms.
SRHM does this by running a demon(called srhmd) on every robot in the swarm that gathers information about the 
health, resource use and sensor data of the robot it is running on and then sends that information to a computer running
an application that process the data and then displays it on a GUI that is updated in real time.  This allows the user to
simply watch the GUI to see the current status of their swarm.  The application is entirely implemeneted in Python 3.
The application also has an autodepolyment feature which is a python script that when run will send srhmd to each of the
robots and start it.

## Installation
From a fesh environment, all dependencies can be installed using

	pip install -r requirements.txt

After installing requirements, the program can be run using

	python driver.py

An instance of the SRHMD can be deployed on to a compatible machine with docker by navigating to the resources subfolder in srhmd and using

	python autodepoly_test.py

## Additional Information
Networking information:

Sending information over networks is handled with the Comms class in this application.  Comms is used to make publishers
and subscribers which are two parts of a connection, the publisher is used to send messages and subscriber is used to recieve
messages.  A connection is created by having one program, which can be on the same or a different machine 
as the other side of the connection, make an subscriber and then another application creates a publisher with the same 
information as the subscriber.  It doesn't matter whether thesubscriber or publisher is created first.  Messages can then be sent between the subscriber and the publisher once they have both been created. As a subscriber Comms gathers 
incoming messages and saves them to a queue that they can later be pulled from.  Comms inteneral uses a library called 
zmq to function.

Config file:
Swarms are saved as config file which is a json file that contains information about the robots in the swarm.
This config file is used by the server side to set up the subscribers that are needed to get data and to set up the
GUI with the correct robot names and fields.  Autodeploy takes this config file and breaks it up and sends only the parts
of the config revelant to the robot it is being sent to.


Application structure:

Client side:
In SRHM the software that code that runs on the robot is considered client side code.  The main file that makes up 
SRHM's client side is srhmd.  Srhmd is a program that that gathers data from the robot it is running on and sends it
to the server side.  Srhmd directly gathers information about the cpu and memory usage and also uses Comms subscribers
to gather information from applications running on the robot.  This means that senor data gathering can be implemeneted 
by having programs that run on the robot and gather the sensors information and create a publisher connected to one of 
srhmd's subscribers.  This way users can implement their own sensors or only download the sensor programs they need.
Srhmd gathers all the data from the sensor programs and the data it gahers itself and then sends it over comms to the
server side.

Server side:
In SRHM the server side is made of the GUI of the application and code that is used to recieve messages from the robots.
The GUI is made up of interface.py and all the files in the gui folder.  The interface.py contains the Gui class which is
used by other classes to interact with the GUI easily.  The Gui class also makes use of the animatedplot.py, 
collapsiblepane.py and infodisplay.py, these files contain code that make it possible to plot incoming data, display
collapsible panes, gui elements that collapse if clicked on when opened and open if clicked on when collapsed, and
displays the information in the GUI that shows the latest data from the robot.  The GUI contains a list of robots and
displays the latest data from the robots below the robot's listing on the GUI.  The GUI also has drop down menus at the top
that can be used to modify the swarm by adding robots, removing robots, loading new swarms and saving the current swarm.
In addition to the GUI the server side also relies on Display.py which contains a class called Display.  The Display class
creates subscribers for each of the robots and saves the information it gets from them before using that new data to update
the GUI.  The final part of the server side is driver.py which is used to start Display and any other services that the
application is using.