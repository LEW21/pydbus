FROM centos:7
RUN yum makecache fast
RUN rpm -Uvh http://download.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-9.noarch.rpm
RUN rpm -Uvh https://centos7.iuscommunity.org/ius-release.rpm

RUN yum -y update
RUN yum upgrade

RUN yum install -y dbus psmisc dbus-x11 python36u  python36-pip python36u-devel pygobject3 pygobject3-devel python3-gobject 
RUN python3.6 --version
RUN pip3.6 install --upgrade pip
RUN pip3.6 install greenlet

ADD . /root/
RUN cd /root && python3.6 setup.py install

RUN /root/tests/run.sh python3.6
