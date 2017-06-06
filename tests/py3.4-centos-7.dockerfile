FROM centos:7
RUN yum makecache fast
RUN rpm -Uvh http://download.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-9.noarch.rpm
RUN yum -y update
RUN yum -y upgrade

RUN yum install -y dbus python3-gi python3-pip psmisc dbus-x11 pygobject3 pygobject3-devel python34 python34-devel
RUN ls /bin/python*
RUN python3 --version
RUN pip3 install greenlet

ADD . /root/
RUN cd /root && python3.4 setup.py install

RUN /root/tests/run.sh python3.4
