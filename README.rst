pydbus
======

Pythonic DBus library.

It's based on PyGI_, the Python GObject Introspection bindings, which is the recommended way to use GLib from Python. Unfortunately, PyGI is not packaged on pypi, so you need to install it from your distribution's repository (usually called python-gi, python-gobject or pygobject3).

It's pythonic!

.. code-block:: python

	from pydbus import SessionBus

	bus = SessionBus()
	notifications = bus.get('.Notifications')

	notifications.Notify('test', 0, 'dialog-information', "Hello World!", "pydbus works :)", [], {}, 5000)

.. code-block:: python

	from pydbus import SystemBus

	bus = SystemBus()
	systemd = bus.get(".systemd1")

	for unit in systemd.ListUnits()[0]:
	    print(unit)

.. _PyGI: https://wiki.gnome.org/PyGObject
