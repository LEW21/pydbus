FROM fedora:22
RUN dnf makecache fast


RUN dnf -y update
RUN dnf -y upgrade

RUN dnf install -y dbus psmisc dbus-x11 python3  python3-pip  python3-devel  pygobject3 pygobject3-devel python3-gobject
RUN python3.4 --version

RUN pip3.4 install --upgrade pip
RUN pip3.4 install greenlet

ADD . /root/
RUN cd /root && python3.4 setup.py install

RUN /root/tests/run.sh python3.4
