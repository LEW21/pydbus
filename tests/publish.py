import sys
from threading import Thread

from gi.repository import GLib

from pydbus import SessionBus


done = 0
loop = GLib.MainLoop()

class TestObject(object):
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
	def __init__(self, iid):
		self.id = iid

	def HelloWorld(self, a, b):
		res = self.id + ": " + a + str(b)
		global done
		done += 1
		if done == 2:
			loop.quit()
		print(res)
		return res

bus = SessionBus()

with bus.publish("net.lew21.pydbus.Test", TestObject("Main"), ("Lol", TestObject("Lol"))):
	remoteMain = bus.get("net.lew21.pydbus.Test")
	remoteLol = bus.get("net.lew21.pydbus.Test", "Lol")

	def t1_func():
		print(remoteMain.HelloWorld("t", 1))

	def t2_func():
		print(remoteLol.HelloWorld("t", 2))

	t1 = Thread(None, t1_func)
	t2 = Thread(None, t2_func)
	t1.daemon = True
	t2.daemon = True

	def handle_timeout():
		print("ERROR: Timeout.")
		sys.exit(1)

	GLib.timeout_add_seconds(200, handle_timeout)

	t1.start()
	t2.start()

	loop.run()

	t1.join()
	t2.join()
