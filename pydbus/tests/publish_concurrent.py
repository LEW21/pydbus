from pydbus import SessionBus
from gi.repository import GLib
from threading import Thread
from pydbus.greenglib.time import sleep
import sys

done = 0
loop = GLib.MainLoop()

log = []

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
	def __init__(self, id):
		self.id = id

	def HelloWorld(self, a, b):
		res = self.id + ": " + a + str(b)

		if b == 1:
			log.append("A(T1)")
			sleep(2) # time for B
			log.append("C(T1)")
		elif b == 2:
			sleep(1) # time for A
			log.append("B(T2)")

		global done
		done += 1
		if done == 2:
			loop.quit()
		print(res)
		return res

with SessionBus() as bus:
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

		GLib.timeout_add_seconds(10, handle_timeout)

		t1.start()
		t2.start()

		loop.run()

		t1.join()
		t2.join()

print(log)
assert(log == ["A(T1)", "B(T2)", "C(T1)"])
