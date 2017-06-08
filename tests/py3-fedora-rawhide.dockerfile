FROM fedora:rawhide
RUN dnf makecache --timer


RUN dnf -y update
RUN dnf -y upgrade

RUN dnf install -y redhat-rpm-config dbus psmisc dbus-x11 python3  python3-pip  python3-devel  pygobject3 pygobject3-devel python3-gobject
RUN python3 --version

RUN pip3 install --upgrade pip
RUN pip3 install greenlet

ADD . /root/
RUN dbus-uuidgen --ensure
RUN cd /root && python3 setup.py install

RUN /root/tests/run.sh python3
