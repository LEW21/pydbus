FROM ubuntu:14.04
RUN apt-get update

RUN apt-get install -y dbus  psmisc dbus-x11 python3  python3-pip python3-dev python3-gi    libglib2.0 libglib2.0-dev gobject-introspection  python-gi-dev
RUN python3.4 --version
RUN pip3 install --upgrade pip
RUN pip3 install greenlet

ADD . /root/
RUN rm -r /root/build
RUN cd /root && python3.4 setup.py install
RUN /root/tests/run.sh python3.4
