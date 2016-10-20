from pydbus import SessionBus, Variant
from gi.repository import GLib
from threading import Thread
import sys

import pytest

from pydbus.tests.util import ClientPool, ClientThread


class DummyObject(object):
	'''
<node>
	<interface name='net.lew21.pydbus.tests.publish_properties'>
		<property name="Foobar" type="s" access="readwrite"/>
		<property name="Foo" type="s" access="read"/>
		<property name="Bar" type="s" access="write"/>
	</interface>
</node>
	'''
	def __init__(self):
		self.Foo = "foo"
		self.Foobar = "foobar"


def test_properties():
	bus = SessionBus()
	loop = GLib.MainLoop()

	with bus.publish("net.lew21.pydbus.tests.publish_properties", DummyObject()):
		remote = bus.get("net.lew21.pydbus.tests.publish_properties")
		remote_iface = remote['net.lew21.pydbus.tests.publish_properties']

		def t1_func():
			for obj in [remote, remote_iface]:
				assert(obj.Foo == "foo")
				assert(obj.Foobar == "foobar")
				obj.Foobar = "barfoo"
				assert(obj.Foobar == "barfoo")
				obj.Foobar = "foobar"
				assert(obj.Foobar == "foobar")
				obj.Bar = "rab"

			remote.Foobar = "barfoo"

			with pytest.raises(GLib.GError):
				remote.Get("net.lew21.pydbus.tests.publish_properties", "Bar")
			with pytest.raises(GLib.GError):
				remote.Set("net.lew21.pydbus.tests.publish_properties", "Foo", Variant("s", "haxor"))
			assert(remote.GetAll("net.lew21.pydbus.tests.publish_properties") == {'Foobar': 'barfoo', 'Foo': 'foo'})

		t1 = ClientThread(t1_func, loop)

		GLib.timeout_add_seconds(2, loop.quit)

		t1.start()

		loop.run()

		# The result is not important, but it might reraise the assertion
		t1.result
