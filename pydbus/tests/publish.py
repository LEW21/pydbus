from pydbus import SessionBus
from gi.repository import GLib
from threading import Thread
import sys

from pydbus.tests.util import ClientPool, ClientThread


class DummyObject(object):
	'''
<node>
	<interface name='net.lvht.Foo1'>
		<method name='HelloWorld'>
			<arg type='s' name='a' direction='in'/>
			<arg type='i' name='b' direction='in'/>
			<arg type='s' name='response' direction='out'/>
		</method>
	</interface>
</node>
	'''
	def __init__(self, id):
		self.id = id

	def HelloWorld(self, a, b):
		res = self.id + ": " + a + str(b)
		return res


def test_multiple_requests():
	loop = GLib.MainLoop()
	bus = SessionBus()

	with bus.publish("net.lew21.pydbus.Test", DummyObject("Main"), ("Lol", DummyObject("Lol"))):
		remoteMain = bus.get("net.lew21.pydbus.Test")
		remoteLol = bus.get("net.lew21.pydbus.Test", "Lol")

		def t1_func():
			return remoteMain.HelloWorld("t", 1)

		def t2_func():
			return remoteLol.HelloWorld("t", 2)

		pool = ClientPool(loop.quit)
		t1 = ClientThread(t1_func, loop, pool)
		t2 = ClientThread(t2_func, loop, pool)

		GLib.timeout_add_seconds(2, loop.quit)

		t1.start()
		t2.start()

		loop.run()

		assert t1.result == "Main: t1"
		assert t2.result == "Lol: t2"
