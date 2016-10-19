FROM ubuntu:14.04
RUN apt-get update

RUN apt-get install -y dbus python-gi python-pip psmisc python-dev
RUN python2 --version
RUN pip2 install greenlet pytest

ADD . /root/
RUN cd /root && python2 setup.py install

RUN /root/tests/run.sh python2 dontpublish
