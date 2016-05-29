FROM ubuntu:16.04
RUN apt-get update

RUN apt-get install -y dbus python-gi python-pip psmisc
RUN python2 --version
RUN pip2 install greenlet

ADD . /root/
RUN cd /root && python2 setup.py install

RUN DBUS_SESSION_BUS_ADDRESS=$(dbus-daemon --session --print-address --fork) python2 -m pydbus.tests.identifier && killall dbus-daemon
RUN DBUS_SESSION_BUS_ADDRESS=$(dbus-daemon --session --print-address --fork) python2 -m pydbus.tests.publish && killall dbus-daemon
RUN DBUS_SESSION_BUS_ADDRESS=$(dbus-daemon --session --print-address --fork) python2 -m pydbus.tests.publish_concurrent && killall dbus-daemon
RUN DBUS_SESSION_BUS_ADDRESS=$(dbus-daemon --session --print-address --fork) python2 -m pydbus.tests.publish_multiface && killall dbus-daemon
