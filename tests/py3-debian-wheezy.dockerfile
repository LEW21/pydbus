FROM debian:wheezy
RUN apt-get update
RUN echo codename 7
RUN apt-get install -y dbus  psmisc dbus-x11 python3  python3-pip python3-dev python3-gi    libglib2.0 libglib2.0-dev gobject-introspection  python-gi-dev
RUN python3 --version
RUN uname -a

RUN pip-3.2 install greenlet ipaddress

ADD . /root/

RUN cd /root && python3 setup.py install
RUN /root/tests/run.sh python3
