pydbus
======

Pythonic DBus library.

It's based on PyGI_, the Python GObject Introspection bindings, which is the recommended way to use GLib from Python. Unfortunately, PyGI is not packaged on pypi, so you need to install it from your distribution's repository (usually called python-gi, python-gobject or pygobject3).

It's pythonic!

And now, it can also publish objects! Changelog: https://github.com/LEW21/pydbus/releases

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

Watch for new systemd jobs
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

	from pydbus import SystemBus
	from gi.repository import GObject

	bus = SystemBus()
	systemd = bus.get(".systemd1")

	systemd.JobNew.connect(print)
	GObject.MainLoop().run()

	# or

	systemd.onJobNew = print
	GObject.MainLoop().run()

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

.. _PyGI: https://wiki.gnome.org/PyGObject
.. _Tutorial: https://github.com/LEW21/pydbus/blob/master/doc/tutorial.rst

Copyright Information
---------------------

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
