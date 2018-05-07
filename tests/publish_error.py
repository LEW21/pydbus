import sys
from threading import Thread
from gi.repository import GLib, Gio
from pydbus import SessionBus
from pydbus.error import register_error, map_error, map_by_default, error_registration

import logging
logger = logging.getLogger('pydbus.registration')
logger.disabled = True

loop = GLib.MainLoop()
DOMAIN = Gio.DBusError.quark()  # TODO: Register new domain.


@register_error("net.lew21.pydbus.tests.ErrorA", DOMAIN, 1000)
class ExceptionA(Exception):
	pass


@register_error("net.lew21.pydbus.tests.ErrorB", DOMAIN, 2000)
class ExceptionB(Exception):
	pass


@map_error("org.freedesktop.DBus.Error.InvalidArgs")
class ExceptionC(Exception):
	pass


@map_by_default
class ExceptionD(Exception):
	pass


class ExceptionE(Exception):
	pass


class TestObject(object):
	'''
<node>
	<interface name='net.lew21.pydbus.tests.TestInterface'>
		<method name='RaiseA'>
			<arg type='s' name='msg' direction='in'/>
		</method>
		<method name='RaiseB'>
			<arg type='s' name='msg' direction='in'/>
		</method>
		<method name='RaiseD'>
			<arg type='s' name='msg' direction='in'/>
		</method>
		<method name='RaiseE'>
			<arg type='s' name='msg' direction='in'/>
		</method>
	</interface>
</node>
	'''

	def RaiseA(self, msg):
		raise ExceptionA(msg)

	def RaiseB(self, msg):
		raise ExceptionB(msg)

	def RaiseD(self, msg):
		raise ExceptionD(msg)

	def RaiseE(self, msg):
		raise ExceptionE(msg)

bus = SessionBus()

with bus.publish("net.lew21.pydbus.tests.Test", TestObject()):
	remote = bus.get("net.lew21.pydbus.tests.Test")

	def t_func():
		# Test new registered errors.
		try:
			remote.RaiseA("Test A")
		except ExceptionA as e:
			assert str(e) == "Test A"

		try:
			remote.RaiseB("Test B")
		except ExceptionB as e:
			assert str(e) == "Test B"

		# Test mapped errors.
		try:
			remote.Get("net.lew21.pydbus.tests.TestInterface", "Foo")
		except ExceptionC as e:
			assert str(e) == "No such property 'Foo'"

		# Test default errors.
		try:
			remote.RaiseD("Test D")
		except ExceptionD as e:
			assert str(e) == "Test D"

		try:
			remote.RaiseE("Test E")
		except ExceptionD as e:
			assert str(e) == "Test E"

		# Test with no default errors.
		error_registration.map_by_default(None)

		try:
			remote.RaiseD("Test D")
		except Exception as e:
			assert not isinstance(e, ExceptionD)

		try:
			remote.RaiseE("Test E")
		except Exception as e:
			assert not isinstance(e, ExceptionD)
			assert not isinstance(e, ExceptionE)

		loop.quit()

	t = Thread(None, t_func)
	t.daemon = True

	def handle_timeout():
		print("ERROR: Timeout.")
		sys.exit(1)

	GLib.timeout_add_seconds(4, handle_timeout)

	t.start()
	loop.run()
	t.join()
