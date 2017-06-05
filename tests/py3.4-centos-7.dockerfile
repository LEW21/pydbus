FROM centos:7
RUN yum makecache fast
RUN yum upgrade

RUN yum install -y dbus python3-gi python3-pip psmisc dbus-x11 pygobject3 pygobject3-devel python34-devel
RUN python3 --version
RUN pip3 install greenlet

ADD . /root/
RUN cd /root && python3 setup.py install

RUN /root/tests/run.sh python3
