from pydbus import SessionBus
from gi.repository import GObject, GLib
from threading import Thread
import sys

done = 0
loop = GObject.MainLoop()

class TestObject(object):
	'''
<node>
	<interface name='net.lew21.pydbus.tests.Iface1'>
		<method name='Method1'>
			<arg type='s' name='response' direction='out'/>
		</method>
	</interface>
	<interface name='net.lew21.pydbus.tests.Iface2'>
		<method name='Method2'>
			<arg type='s' name='response' direction='out'/>
		</method>
	</interface>
</node>
	'''
	def Method1(self):
		global done
		done += 1
		if done == 2:
			loop.quit()
		return ("M1",)

	def Method2(self):
		global done
		done += 1
		if done == 2:
			loop.quit()
		return ("M2",)

with SessionBus() as bus:
	with bus.expose("net.lew21.pydbus.tests.expose_multiface", TestObject()):
		remote = bus.get("net.lew21.pydbus.tests.expose_multiface")

		def t1_func():
			print(remote.Method1())
			print(remote.Method2())

		t1 = Thread(None, t1_func)
		t1.daemon = True

		def handle_timeout():
			print("ERROR: Timeout.")
			sys.exit(1)

		GLib.timeout_add_seconds(2, handle_timeout)

		t1.start()

		loop.run()

		t1.join()
