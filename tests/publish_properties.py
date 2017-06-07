import sys
from threading import Thread

from gi.repository import GLib

from pydbus import SessionBus, Variant


done = 0
loop = GLib.MainLoop()

class TestObject(object):
	'''
<node>
	<interface name='net.lew21.pydbus.tests.publish_properties'>
		<property name="Foobar" type="s" access="readwrite"/>
		<property name="Foo" type="s" access="read"/>
		<property name="Bar" type="s" access="write"/>
		<method name='Quit'/>
	</interface>
</node>
	'''
	def __init__(self):
		self.Foo = "foo"
		self.Foobar = "foobar"

	def Quit(self):
		loop.quit()

bus = SessionBus()

with bus.publish("net.lew21.pydbus.tests.publish_properties", TestObject()):
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

		try:
			remote.Get("net.lew21.pydbus.tests.publish_properties", "Bar")
			assert(False)
		except GLib.GError:
			pass
		try:
			remote.Set("net.lew21.pydbus.tests.publish_properties", "Foo", Variant("s", "haxor"))
			assert(False)
		except GLib.GError:
			pass
		assert(remote.GetAll("net.lew21.pydbus.tests.publish_properties") == {'Foobar': 'barfoo', 'Foo': 'foo'})
		print("Just before quit.")
		remote.Quit()

	t1 = Thread(None, t1_func)
	t1.daemon = True

	def handle_timeout():
		print("ERROR: Timeout.")
		sys.exit(1)

	GLib.timeout_add_seconds(20, handle_timeout)

	t1.start()

	loop.run()

	t1.join()
