FROM ubuntu:14.04
RUN apt-get update

RUN apt-get install -y dbus python3-gi python3-pip psmisc python3-dev dbus-x11 python-gi-dev python3.4 libglib2.0 libglib2.0-dev
RUN python3.4 --version
RUN pip3 install --upgrade pip
RUN pip3 install greenlet

ADD . /root/
RUN ls -lR .
RUN cd /root && python3.4 setup.py install

RUN /root/tests/run.sh python3.4
