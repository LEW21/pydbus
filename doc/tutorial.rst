===============
pydbus tutorial
===============

:Author: `Linus Lewandowski`_
:Based on: python-dbus tutorial by Simon McVittie, `Collabora Ltd.`_ (2006-06-14)
:Date: 2016-09-26

.. _`Collabora Ltd.`: http://www.collabora.co.uk/
.. _`Linus Lewandowski`: http://lew21.net/

This tutorial requires Python 2.7 or up, and ``pydbus`` 0.6 or up.

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

D-Bus objects
=============

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

All objects have methods, properties and signals.

Setting up an event loop
========================

To handle signals emitted by exported objects, to asynchronously call methods
or to export your own objects, you need to setup an event loop.

The only main loop supported by ``pydbus`` is GLib.MainLoop.

GLib.MainLoop
-------------

To create the loop object use::

    from gi.repository import GLib

    loop = GLib.MainLoop()

To execute the loop use::

    loop.run()

While ``loop.run()`` is executing, GLib will watch for signals you're subscribed to, or accesses to objects you exported, and execute correct callbacks when appropriate. To stop, call ``loop.quit()``.

.. _proxy object:

Accessing exported objects
==========================

To interact with a remote object, you use a *proxy object*. This is a
Python object which acts as a proxy or "stand-in" for the remote object -
when you call a method on a proxy object, this causes dbus-python to make
a method call on the remote object, passing back any return values from
the remote object's method as the return values of the proxy method call.

Obtaining proxy objects
-----------------------

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
    dev = bus.get('.NetworkManager', 'Devices/0')

Object API
-----------

To see the API of a specific proxy object, use help()::

    help(dev)

To call a method::

    dev.Disconnect()

To asynchronously call a method::

    def print_result(returned=None, error=None):
        print(returned, error)

    dev.GetAppliedConnection(0, callback=print_result)
    loop.run()

To read a property::

    print(dev.Autoconnect)

To set a property::

    dev.Autoconnect = True

.. _signal.connect:

To subscribe to a signal::

    dev.StateChanged.connect(print)
    loop.run()

connect() returns a Subscription object with a disconnect() method, that can be used to stop watching the signal. Also, it can be used as a context manager (with the ''with'' statement), to automatically disconnect at the end of the scope.

.. _onSignal:

Alternatively, you can set the on`Signal` property::

    dev.onStateChanged = print
    loop.run()

This way, you can unsubscribe from the signal by setting the property to None.

However, don't mix subscriptions in one of those ways with unsubscribtions
in another, it won't work.

See also
~~~~~~~~

See the examples in ``examples/systemctl.py`` and ``tests/gnome_music.py``.

Interfaces
----------
D-Bus uses *interfaces* to provide a namespacing mechanism for methods,
signals and properties. An interface is a group of related methods, signals
and properties, identified by a name which is a series of dot-separated components
starting with a reversed domain name. For instance, each NetworkManager_
object representing a network interface implements the interface
``org.freedesktop.NetworkManager.Device``, which has methods like
``Disconnect``.

An object may have multiple interfaces. They may be incompatible, for example
when using some sort of API versioning. By default, pydbus merges all the
interfaces to offer a single proxy object's API, but it's possible to obtain
a view providing only a single interface::

    dev = bus.get('.NetworkManager', 'Devices/0')
    dev_api = dev['org.freedesktop.NetworkManager.Device']

You may use all of the proxy object members described in the previous chapter
on the dev_api too.

.. _bus.subscribe:

Signal matching
---------------

You may also match the signals using a pattern.
See ``help(bus.subscribe)`` for more details.

.. --------------------------------------------------------------------

Exporting own objects
=====================

Objects made available to other applications over D-Bus are said to be
*exported*.

To export objects, the Bus needs to be connected to an event loop - see
section `Setting up an event loop`_. Exported methods will only be called,
and queued signals will only be sent, while the event loop is running.

Class preparation
-----------------

To prepare a class for exporting on the Bus, provide the dbus introspection XML
in a ''dbus'' class property or in its ''docstring''. For example::

    from pydbus.generic import signal

    class Example(object):
      """
        <node>
          <interface name='net.lew21.pydbus.TutorialExample'>
            <method name='EchoString'>
              <arg type='s' name='a' direction='in'/>
              <arg type='s' name='response' direction='out'/>
            </method>
            <property name="SomeProperty" type="s" access="readwrite">
              <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
          </interface>
        </node>
      """

      def EchoString(self, s):
        """returns whatever is passed to it"""
        return s

      def __init__(self):
        self._someProperty = "initial value"

      @property
      def SomeProperty(self):
        return self._someProperty

      @SomeProperty.setter
      def SomeProperty(self, value):
        self._someProperty = value
        self.PropertiesChanged("net.lew21.pydbus.TutorialExample", {"SomeProperty": self.SomeProperty}, [])

      PropertiesChanged = signal()

If you don't want to put XML in a Python file, you can add XML files to your Python package and use them this way::

    import pkg_resources

    ifaces = ["org.mpris.MediaPlayer2", "org.mpris.MediaPlayer2.Player", "org.mpris.MediaPlayer2.Playlists", "org.mpris.MediaPlayer2.TrackList"]
    MediaPlayer2.dbus = [pkg_resources.resource_string(__name__, "mpris/" + iface + ".xml").decode("utf-8") for iface in ifaces]


.. _bus.publish:

Object publication
------------------

To publish an object, use the ``bus.publish`` method::

    bus.publish("net.lew21.pydbus.TutorialExample", Example())
    loop.run()

Here, publish() both binds the service to the net.lew21.pydbus.TutorialExample
bus name, and exports the object as /net/lew21/pydbus/TutorialExample.

Note, that you can use the publish() method only once per a bus name
that you want to bind. However, you can use it to export multiple objects
- by passing them in additional parameters to the method::

    bus.publish("net.lew21.pydbus.TutorialExample",
      Example(),
      ("Subdir1", Example()),
      ("Subdir2", Example()),
      ("Subdir2/Whatever", Example())
    )
    loop.run()

The 2nd, 3rd, ... arguments can be objects or tuples of a path and a object.
``bus.publish()`` uses the same path-deducing (and bus-name-deducing) logic that's
used in ``bus.get()``, so you may use relative paths or absolute paths, depending
on your needs.

Like ``signal.connect()``, ``bus.publish()`` returns an object with an ``unpublish()``
method, that can be used as a context manager.

See also
~~~~~~~~

See the example in ``examples/clientserver/server.py``.

.. _bus.request_name:
.. _bus.register_object:

Lower level API
---------------

Sometimes, you can't just publish everything in one call, you need more control
over the process of binding a name and exporting single objects.

In this case, you can use ``bus.request_name()`` and ``bus.register_object()`` yourself.
See ``help(bus.request_name)`` and ``help(bus.register_object)`` for details.

.. --------------------------------------------------------------------

Data types
==========

Unlike Python, D-Bus is statically typed. Each method and signal takes arguments of predefined types; each method returns value(s) of predefined types; and each property has a predefined type. You can't dynamically change those types.

D-Bus has an introspection mechanism, which ``pydbus`` uses to discover
the correct argument types. Python types are converted into the right
D-Bus data types automatically, if possible; ``TypeError`` is raised
if the type is inappropriate.

Container types
---------------

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
-------------

If a D-Bus method returns no value, the Python proxy method will return ``None``.

If a D-Bus method returns a single value, it will be returned directly.

Otherwise, Python proxy method will return a tuple containing all the values.

.. --------------------------------------------------------------------

License for this document
=========================

Copyright 2006-2007 `Collabora Ltd.`_

Copyright 2016 `Linus Lewandowski`_

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
