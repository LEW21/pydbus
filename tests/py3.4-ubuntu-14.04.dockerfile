FROM ubuntu:14.04
RUN apt-get update

RUN apt-get install -y dbus python3-gi python3-pip psmisc python3-dev
RUN python3 --version
RUN pip3 install greenlet pytest

ADD . /root/
RUN cd /root && python3 setup.py install

RUN /root/tests/run.sh python3 dontpublish
