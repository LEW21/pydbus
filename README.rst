pydbus
======
.. image:: https://travis-ci.org/hcoin/pydbus.svg?branch=master
    :target: https://travis-ci.org/hcoin/pydbus
.. image:: https://badge.fury.io/py/pydbus.svg
    :target: https://badge.fury.io/py/pydbus
.. image:: https://readthedocs.org/projects/pydbus/badge/?version=latest
    :target: http://pydbus.readthedocs.io/en/latest/?badge=latest

Publish DBus services or access DBus clients no differently
than you would a typical local Python method, property or signal callback.
 
For example:

.. code-block:: python

    ...
    sb = SystemBus()
    NetworkManager = sb.get("org.freedesktop.NetworkManager",translation_spec=True)
    r=NetworkManager.CheckpointCreate(devices=['/org/freedesktop/NetworkManager/Devices/0'],
        rollback_timeout = 10, flags = "DELETE_NEW_CONNECTIONS")
      
Notice the use of argument names instead of only by position (which still works),
string values for flags instead of cryptic integers.  No
need for DBus specific function decorations. Should a method return be a list of
named values, call it ret, then

.. code-block:: python

    ret[argposition_number] == arg['argument_name'] == arg.argument_name 

There are many other 'pythonic conveniences', for instance using the example
above, after the function returns, NetworkManager._state.rollback == 10, etc.

Documentation: http://pydbus.readthedocs.io/en/latest
 
Changelog: https://github.com/hcoin/pydbus


Requirements
------------
* Python 3.2+
* Supports: Debian Jessie to sid.  Fedora 22 to rawhide.  Centos 7 (python 3.4 and 3.6). Ubuntu 14.04  thru 16.04
* See tests/py<your distro and version>.dockerfile for tested installation examples.

Note: Supports full dbus publishing and access on all distros, even pre Glib v2.46.



Copyright Information
---------------------

Documentation, argument name/value translator, unit testing, _state extension, publishing across distros,

Copyright (C) 2017 Harry Coin, Quiet Fountain LLC <hcoin@quietfountain.com>

Modules pre-June 2016

Copyright (C) 2014, 2015, 2016 Linus Lewandowski <linus@lew21.net>


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
