==============
Short Examples
==============


---------------------------------
Useful background documentation:
---------------------------------

  _PyGI: https://wiki.gnome.org/Projects/PyGObject
  _GLib: https://developer.gnome.org/glib/
  _girepository: https://wiki.gnome.org/Projects/GObjectIntrospection


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
