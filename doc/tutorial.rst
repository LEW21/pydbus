===============
pydbus tutorial
===============

:Author: `Janusz Lewandowski`_
:Based on: python-dbus tutorial by Simon McVittie, `Collabora Ltd.`_ (2006-06-14)
:Date: 2016-02-29

.. _`Collabora Ltd.`: http://www.collabora.co.uk/
.. _`Janusz Lewandowski`: http://lew21.net/

This tutorial requires Python 2.7 or up, and ``pydbus`` 0.4 or up.

.. contents::

.. --------------------------------------------------------------------

.. _Bus object:
.. _Bus objects:

Connecting to the Bus
=====================

Applications that use D-Bus typically connect to a *bus daemon*, which
forwards messages between the applications. To use D-Bus, you need to create a
``Bus`` object representing the connection to the bus daemon.

There are generally two bus daemons you may be interested in. Each user
login session should have a *session bus*, which is local to that
session. It's used to communicate between desktop applications. Connect
to the session bus by creating a ``SessionBus`` object::

    from pydbus import SessionBus

    session_bus = SessionBus()

The *system bus* is global and usually started during boot; it's used to
communicate with system services like systemd_, udev_ and NetworkManager_.
To connect to the system bus, create a ``SystemBus`` object::

    from pydbus import SystemBus

    system_bus = SystemBus()

Of course, you can connect to both in the same application.

For special purposes, you might use a non-default Bus using the Bus class.

.. _systemd:
    https://www.freedesktop.org/wiki/Software/systemd/
.. _udev:
    https://www.kernel.org/pub/linux/utils/kernel/hotplug/udev/udev.html
.. _NetworkManager:
    https://wiki.gnome.org/Projects/NetworkManager

.. --------------------------------------------------------------------

Making method calls
===================

D-Bus applications can export objects for other applications' use. To
start working with an object in another application, you need to know:

* The *bus name*. This identifies which application you want to
  communicate with. You'll usually identify applications by a
  *well-known name*, which is a dot-separated string starting with a
  reversed domain name, such as ``org.freedesktop.NetworkManager``
  or ``com.example.WordProcessor``.

* The *object path*. Applications can export many objects - for
  instance, example.com's word processor might provide an object
  representing the word processor application itself and an object for
  each document window opened, or it might also provide an object for
  each paragraph within a document.
  
  To identify which one you want to interact with, you use an object path,
  a slash-separated string resembling a filename. For instance, example.com's
  word processor might provide an object at ``/`` representing the word
  processor itself, and objects at ``/documents/123`` and
  ``/documents/345`` representing opened document windows.

As you'd expect, one of the main things you can do with remote objects
is to call their methods. As in Python, methods may have parameters,
and they may return one or more values.

.. _proxy object:

Proxy objects
-------------

To interact with a remote object, you use a *proxy object*. This is a
Python object which acts as a proxy or "stand-in" for the remote object -
when you call a method on a proxy object, this causes dbus-python to make
a method call on the remote object, passing back any return values from
the remote object's method as the return values of the proxy method call.

.. _bus.get:

To obtain a proxy object, call the ``get`` method on the ``Bus``.
For example, NetworkManager_ has the well-known name
``org.freedesktop.NetworkManager`` and exports an object whose object
path is ``/org/freedesktop/NetworkManager``, plus an object per network
interface at object paths like
``/org/freedesktop/NetworkManager/Devices/eth0``. You can get a proxy
for the object representing eth0 like this::

    from pydbus import SystemBus
    bus = SystemBus()
    proxy = bus.get('org.freedesktop.NetworkManager',
                           '/org/freedesktop/NetworkManager/Devices/0')

pydbus has implemented shortcuts for the most common cases. If you
start the bus name with "." (".NetworkManager"), "org.freedesktop" will
become automatically prepended. If you specify a relative object path
(without the leading "/"), the bus name transformed to a path format
will get prepended ("/org/freedesktop/NetworkManager/"). If you don't
specify the object path at all, the transformed bus name will be used
automatically ("/org/freedesktop/NetworkManager"). Therefore, you may
rewrite the above code as::

    from pydbus import SystemBus
    bus = SystemBus()
    proxy = bus.get('.NetworkManager', 'Devices/0')

Interfaces and methods
----------------------

D-Bus uses *interfaces* to provide a namespacing mechanism for methods.
An interface is a group of related methods and signals (more on signals
later), identified by a name which is a series of dot-separated components
starting with a reversed domain name. For instance, each NetworkManager_
object representing a network interface implements the interface
``org.freedesktop.NetworkManager.Device``, which has methods like
``Disconnect``.

To call a method, call the method of the same name on the proxy object::

    from pydbus import SystemBus
    bus = SystemBus()
    dev = bus.get('.NetworkManager', 'Devices/0')
    dev.Disconnect()

An object may have multiple interfaces. They may be incompatible, for example
when using some sort of API versioning. By default, pydbus merges all the
interfaces to offer a single proxy object's API, but it's possible to obtain
a view providing only a single interface::

    dev = bus.get('.NetworkManager', 'Devices/0')
    dev_api = dev['org.freedesktop.NetworkManager.Device']

See also
~~~~~~~~

See the example in ``pydbus/examples/systemctl.py``.

Data types
----------

Unlike Python, D-Bus is statically typed - each method has a certain
*signature* representing the types of its arguments, and will not accept
arguments of other types.

D-Bus has an introspection mechanism, which ``pydbus`` uses to discover
the correct argument types. Python types are converted into the right
D-Bus data types automatically, if possible; ``TypeError`` is raised
if the type is inappropriate.

Container types
~~~~~~~~~~~~~~~

D-Bus supports four container types: array (a variable-length sequence of the
same type), struct (a fixed-length sequence whose members may have
different types), dictionary (a mapping from values of the same basic type to
values of the same type), and variant (a container which may hold any
D-Bus type, including another variant).

Arrays are represented by Python lists. The signature of an array is 'ax'
where 'x' represents the signature of one item. For instance, you could
also have 'as' (array of strings) or 'a(ii)' (array of structs each
containing two 32-bit integers).

Structs are represented by Python tuples. The signature of a struct
consists of the signatures of the contents, in parentheses - for instance
'(is)' is the signature of a struct containing a 32-bit integer and a string.

Dictionaries are represented by Python dictionaries.
The signature of a dictionary is 'a{xy}' where 'x' represents the
signature of the keys (which may not be a container type) and 'y'
represents the signature of the values. For instance,
'a{s(ii)}' is a dictionary where the keys are strings and the values are
structs containing two 32-bit integers.

Return values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a D-Bus method returns no value, the Python proxy method will return
``None``. Otherwise, Python proxy method will return a tuple containing those values.

.. --------------------------------------------------------------------

Receiving signals
=================

To receive signals, the Bus needs to be connected to an event loop.
Signals will only be received while the event loop is running.

Setting up an event loop
------------------------

The only main loop supported by ``pydbus`` is GLib's GObject.MainLoop.

Actually starting the main loop is as usual for ``pygi``::

    from gi.repository import GObject

    loop = GObject.MainLoop()
    loop.run()

While ``loop.run()`` is executing, GLib will run your callbacks when
appropriate. To stop, call ``loop.quit()``.

.. _signal.connect:

Signal handling
---------------

To respond to signals, you can use the ``connect`` method on
the suitable signal property of an proxy object::

    systemd.JobNew.connect(print)
    loop.run()

It returns a Subscription object with a unsubscribe() (+ disconnect() alias)
method, that can be used to stop watching the signal. Also, it can be used
as a context manager (with the ''with'' statement), to automatically disconnect
at the end of the scope.

.. _onSignal:

Alternatively, you can set the on`Signal` property::

    systemd.onJobNew = print
    loop.run()

This way, you can unsubscribe from the signal by setting the property to None.

However, don't mix subscriptions in one of those ways with unsubscribtions
in another, it won't work.

.. _bus.subscribe:

Signal matching
---------------

You may also match the signals using a pattern.
See ``help(bus.subscribe)`` for more details.

.. --------------------------------------------------------------------

Exporting objects
=================

Objects made available to other applications over D-Bus are said to be
*exported*.

To export objects, the Bus needs to be connected to an event loop - see
section `Setting up an event loop`_. Exported methods will only be called,
and queued signals will only be sent, while the event loop is running.

Service class preparation
-------------------------

To prepare a class for exporting on the Bus, provide the dbus introspection XML
in a ''dbus'' class property or in its ''docstring''. For example::

    class Example(object):
      """
        <node>
          <interface name='net.lew21.pydbus.TutorialExample'>
            <method name='EchoString'>
              <arg type='s' name='a' direction='in'/>
              <arg type='s' name='response' direction='out'/>
            </method>
          </interface>
        </node>
      """
    
      def EchoString(self, s):
        """returns whatever is passed to it"""
        return (s,)

.. _bus.expose:

Object exposure
---------------

To expose an object, use the ``bus.expose`` method::

    bus.expose("net.lew21.pydbus.TutorialExample", Example())
    loop.run()

Here, expose() both binds the service to the net.lew21.pydbus.TutorialExample
bus name, and exports the object as /net/lew21/pydbus/TutorialExample.

Note, that you can use the expose() method only once per a bus name
that you want to bind. However, you can use it to export multiple objects
- by passing them in additional parameters to the method::

    bus.expose("net.lew21.pydbus.TutorialExample", 
      Example(),
      ("Subdir1", Example()),
      ("Subdir2", Example()),
      ("Subdir2/Whatever", Example())
    )
    loop.run()

The 2nd, 3rd, ... arguments can be objects or tuples of a path and a object.
``bus.expose()`` uses the same path-deducing (and bus-name-deducing) logic that's
used in ``bus.get()``, so you may use relative paths or absolute paths, depending
on your needs.

Like ``signal.connect()``, ``bus.expose()`` returns an object with an ``unexpose()``
method, that can be used as a context manager.

Example
-------

See the example in ``pydbus/examples/clientserver/server.py``.

.. _bus.own_name:
.. _bus.register:

Lower level API
---------------

Sometimes, you can't just expose everything in one call, you need more control
over the process of binding a name and exporting single objects.

In this case, you can use ``bus.own_name()`` and ``bus.register()`` yourself.
See ``help(bus.own_name)`` and ``help(bus.register)`` for details.

.. --------------------------------------------------------------------

License for this document
=========================

Copyright 2006-2007 `Collabora Ltd.`_

Copyright 2016 `Janusz Lewandowski`_

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

..
  vim:set ft=rst sw=4 sts=4 et tw=72:
