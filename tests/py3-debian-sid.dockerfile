FROM debian:sid
RUN echo deb http://http.us.debian.org/debian unstable main contrib non-free > /etc/apt/sources.list
RUN echo deb-src http://http.us.debian.org/debian unstable main contrib non-free >> /etc/apt/sources.list
RUN echo deb http://mirrors.kernel.org/debian unstable main contrib non-free >> /etc/apt/sources.list
RUN echo deb-src http://mirrors.kernel.org/debian unstable main contrib non-free >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y dbus  psmisc dbus-x11 python3  python3-pip python3-dev python3-gi    libglib2.0 libglib2.0-dev gobject-introspection  python-gi-dev
RUN python3 --version
RUN pip3 install --upgrade pip
RUN pip3 install greenlet

ADD . /root/

RUN cd /root && python3 setup.py install
RUN /root/tests/run.sh python3
