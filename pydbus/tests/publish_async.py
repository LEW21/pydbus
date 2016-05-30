#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Anselm Kruis
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#

"""
A variant of publish, that works asynchronously and authorizes the service using Polkit
"""


from __future__ import print_function, absolute_import
from pydbus import SessionBus
from pydbus.authorization import PolkitAuthorization
from gi.repository import GObject, GLib, Polkit, Gio
from threading import Thread
import sys
import traceback

dot_count = 0
done = 0
loop = GObject.MainLoop()


class TestObject(object):
	'''
<node>
	<interface name='net.lvht.Foo1'>
			<method name='HelloWorld1'>
					<arg type='s' name='a' direction='in'/>
					<arg type='i' name='b' direction='in'/>
					<arg type='s' name='response' direction='out'/>
			</method>
			<method name='HelloWorld2'>
					<arg type='s' name='a' direction='in'/>
					<arg type='i' name='b' direction='in'/>
					<arg type='s' name='response' direction='out'/>
			</method>
	</interface>
</node>
	'''

	def __init__(self, id):
		self.id = id

	def do_cancel(self, cancellable):
		print("Timeout, canceling operation")
		sys.stdout.flush()
		cancellable.cancel()

	# the simple way
	@PolkitAuthorization("org.freedesktop.policykit.exec")
	def HelloWorld1(self, a, b, polkit_is_authorized):
		global done
		done += 1
		if done == 2:
			GLib.idle_add(loop.quit)
		if not polkit_is_authorized:
			raise PolkitAuthorization.NotAuthorizedError("You are not authorized!")
		res = self.id + ": " + a + str(b)
		print(res)
		return res

	# use the low level API, otherwise the same as HelloWorld1
	def HelloWorld2(self, a, b, dbus_method_invocation, dbus_bus):
		try:
			cancellable = Gio.Cancellable()
			state = dict(a=a,
						b=b,
						method_invocation=dbus_method_invocation,
						bus=dbus_bus,
						cancellable=cancellable)
			GLib.timeout_add(dbus_bus.timeout, self.do_cancel, cancellable)
			Polkit.Authority.get_async(cancellable, self._cb_get_authority_ready, state)
		except Exception as e:
			traceback.print_exc()
			dbus_method_invocation.return_exception(e)
	HelloWorld2.async = True

	def _cb_get_authority_ready(self, source_object, res, state):
		# source_object is None
		dbus_bus = state['bus']
		dbus_method_invocation = state['method_invocation']
		cancellable = state['cancellable']

		try:
			authority = Polkit.Authority.get_finish(res)
			assert authority is not None

			sender = dbus_method_invocation.get_sender()
			dbus_service = dbus_bus.get('.DBus')['']
			sender_pid = dbus_service.GetConnectionUnixProcessID(sender)  # synchronous call for now
			state['sender_pid'] = sender_pid
			subject = Polkit.UnixProcess.new(sender_pid)

			authority.check_authorization(subject,
										"org.freedesktop.policykit.exec",  # uses auth_admin
										None,
										Polkit.CheckAuthorizationFlags.ALLOW_USER_INTERACTION,
										cancellable,
										self._cb_check_authorization_ready,
										state)
		except Exception as e:
			traceback.print_exc()
			dbus_method_invocation.return_exception(e)

	def _cb_check_authorization_ready(self, authority, res, state):
		dbus_method_invocation = state['method_invocation']
		a = state['a']
		b = state['b']
		sender_pid = state['sender_pid']
		try:
			global done
			done += 1
			if done == 2:
				GLib.idle_add(loop.quit)

			result = authority.check_authorization_finish(res)
			if not result.get_is_authorized():
				dbus_method_invocation.return_dbus_error("unknown.PermissionDenied", "You are not authorized!")
				return

			res = self.id + ": " + a + str(b) + " sender pid " + str(sender_pid)
			print(res)
			dbus_method_invocation.return_value(res)

		except Exception as e:
			traceback.print_exc()
			dbus_method_invocation.return_exception(e)


def print_dots():
	"""Print one dot per second, if the mainloop is running"""
	global dot_count
	print(".", end='')
	dot_count += 1
	if dot_count >= 80:
		print("")
		dot_count = 0
	sys.stdout.flush()
	return True

with SessionBus(timeout=30 * 1000) as bus:
	with bus.publish("net.lew21.pydbus.Test", TestObject("Main"), ("Lol", TestObject("Lol"))):
		remoteMain = bus.get("net.lew21.pydbus.Test")
		remoteLol = bus.get("net.lew21.pydbus.Test", "Lol")

		def t1_func():
			print(remoteMain.HelloWorld1("t", 1))

		def t2_func():
			print(remoteLol.HelloWorld2("t", 2))

		t1 = Thread(None, t1_func)
		t2 = Thread(None, t2_func)
		t1.daemon = True
		t2.daemon = True

		t1.start()
		t2.start()

		GLib.timeout_add_seconds(1, print_dots)

		loop.run()

		t1.join()
		t2.join()
