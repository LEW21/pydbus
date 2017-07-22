pydbus
======
.. image:: https://travis-ci.org/hcoin/pydbus.svg?branch=master
    :target: https://travis-ci.org/hcoin/pydbus
.. image:: https://badge.fury.io/py/pydbus.svg
    :target: https://badge.fury.io/py/pydbus
.. image:: https://readthedocs.org/projects/pydbus/badge/?version=latest
    :target: http://pydbus.readthedocs.io/en/latest/?badge=latest

tl,dr: When accessing a dbus path, if you enable a dictionary for these
routines that describes anything special about it, all the dbus-specific issues
are invisibly managed so well it appears as if it was written from the ground
up as a local python routine. It's very hard to tell the difference between a
local python method, property or signal vs. one handled by a partner over the
dbus. Given a well written translation spec, the user need know nothing further
about dbus operations.

Changelog: https://github.com/hcoin/pydbus

Requirements
------------
* Python 3.2+
* Supports: Debian Jessie to sid.  Fedora 22 to rawhide.  Centos 7 (python 3.4 and 3.6). Ubuntu 14.04  thru 16.04
* See py<your distro and version>.dockerfile for tested installation instructions.

Now supports full dbus publishing and access on all versions.
~~

.. _PyGI: https://wiki.gnome.org/Projects/PyGObject
.. _GLib: https://developer.gnome.org/glib/
.. _girepository: https://wiki.gnome.org/Projects/GObjectIntrospection


Getting Started and Documentation
---------------------------------
https://github.com/hcoin/pydbus/wiki


Examples
--------

Send a desktop notification
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

	from pydbus import SessionBus

	bus = SessionBus()
	notifications = bus.get('.Notifications')

	notifications.Notify('test', 0, 'dialog-information', "Hello World!", "pydbus works :)", [], {}, 5000)

List systemd units
~~~~~~~~~~~~~~~~~~
.. code-block:: python

	from pydbus import SystemBus

	bus = SystemBus()
	systemd = bus.get(".systemd1")

	for unit in systemd.ListUnits():
	    print(unit)
	    
Handle flags and states natively
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

	from pydbus import SystemBus
	from tests.nmdefines import PydbusNetworkManagerSpec,NM_DBUS_INTERFACE,NM_DBUS_INTERFACE_DEVICE
	
    bus=SystemBus()
    #old C way
    nm=bus.get("org.freedesktop.NetworkManager",'Devices/0')["org.freedesktop.NetworkManager.Device"]
    print(str(nm.Capabilities) + ", "+str(nm.DeviceType))
    #7, 14
    
    #pythonic way
    nm_trans=bus.get(NM_DBUS_INTERFACE,'Devices/0',translation_spec=PydbusNetworkManagerSpec)[NM_DBUS_INTERFACE_DEVICE]
    print(str(nm_trans.Capabilities) + ", "+str(nm_trans.DeviceType))
    #('NM_SUPPORTED', 'CARRIER_DETECT', 'IS_SOFTWARE'), GENERIC

Start or stop systemd unit
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

	from pydbus import SystemBus

	bus = SystemBus()
	systemd = bus.get(".systemd1")

	job1 = systemd.StopUnit("ssh.service", "fail")
	job2 = systemd.StartUnit("ssh.service", "fail")

Watch for new systemd jobs
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

	from pydbus import SystemBus
	from gi.repository import GLib

	bus = SystemBus()
	systemd = bus.get(".systemd1")

	systemd.JobNew.connect(print)
	GLib.MainLoop().run()

	# or

	systemd.onJobNew = print
	GLib.MainLoop().run()

View object's API
~~~~~~~~~~~~~~~~~
.. code-block:: python

	from pydbus import SessionBus

	bus = SessionBus()
	notifications = bus.get('.Notifications')

	help(notifications)

More examples & documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


The Tutorial_ contains more examples and docs.

.. _Tutorial: https://github.com/LEW21/pydbus/blob/master/doc/tutorial.rst
.. _Dbus <-> python translation use intro: https://github.com/hcoin/pydbus/blob/master/doc/autotranslator_tutorial.rst
.. _Full Dbus <-> python translation system / spec:  https://github.com/hcoin/pydbus/wiki

Copyright Information
---------------------


Copyright (C) 2014, 2015, 2016 Linus Lewandowski <linus@lew21.net>

wiki, translator.py, nmdefines.py and autotranslator_tutorial.rst
Copyright (C) 2017 Quiet Fountain LLC <hcoin@quietfountain.com>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
