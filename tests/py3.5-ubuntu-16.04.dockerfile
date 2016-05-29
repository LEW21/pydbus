FROM ubuntu:16.04
RUN apt-get update

RUN apt-get install -y dbus python3-gi python3-pip psmisc
RUN python3 --version
RUN pip3 install greenlet

ADD . /root/
RUN cd /root && python3 setup.py install

RUN DBUS_SESSION_BUS_ADDRESS=$(dbus-daemon --session --print-address --fork) python3 -m pydbus.tests.identifier && killall dbus-daemon
RUN DBUS_SESSION_BUS_ADDRESS=$(dbus-daemon --session --print-address --fork) python3 -m pydbus.tests.publish && killall dbus-daemon
RUN DBUS_SESSION_BUS_ADDRESS=$(dbus-daemon --session --print-address --fork) python3 -m pydbus.tests.publish_concurrent && killall dbus-daemon
RUN DBUS_SESSION_BUS_ADDRESS=$(dbus-daemon --session --print-address --fork) python3 -m pydbus.tests.publish_multiface && killall dbus-daemon
