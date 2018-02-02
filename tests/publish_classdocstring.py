from pydbus import SessionBus
from gi.repository import GLib
from threading import Thread
import sys
from time import sleep

loop = GLib.MainLoop()

class TestObject:
	'''
<node>
	<interface name='net.lew21.pydbus.tests.Iface1'>
		<method name='Method1'>
			<arg type='s' name='response' direction='out'/>
		</method>
	</interface>
</node>
	'''
	def Method1(self):
		sleep(1)
		loop.quit()
		return "Passed!"

bus = SessionBus()

with bus.publish("net.lew21.pydbus.tests.publish_classdocstring", TestObject()):
	remote = bus.get("net.lew21.pydbus.tests.publish_classdocstring")

	def closer():
		print(remote.Method1())

	t1 = Thread(None, closer)

	def handle_timeout():
		print("ERROR: Timeout.")
		sys.exit(1)

	GLib.timeout_add_seconds(2, handle_timeout)

	t1.start()

	loop.run()

	t1.join()
