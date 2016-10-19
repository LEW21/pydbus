FROM ubuntu:16.04
RUN apt-get update

RUN apt-get install -y dbus python-gi python-pip psmisc
RUN python2 --version
RUN pip2 install greenlet pytest

ADD . /root/
RUN cd /root && python2 setup.py install

RUN /root/tests/run.sh python2
