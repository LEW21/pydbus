from pydbus import SessionBus
from gi.repository import GLib
from threading import Thread
import sys

done = 0
loop = GLib.MainLoop()

class TestObject(object):
	'''
<node>
	<interface name='net.lew21.pydbus.tests.publish_async'>
		<method name='HelloWorld'>
			<arg type='i' name='x' direction='in'/>
			<arg type='s' name='response' direction='out'/>
		</method>
	</interface>
</node>
	'''
	def __init__(self, id):
		self.id = id

	def HelloWorld(self, x):
		res = self.id + ": " + str(x)
		print(res)
		return res

bus = SessionBus()

with bus.publish("net.lew21.pydbus.tests.publish_async", TestObject("Obj")):
	remote = bus.get("net.lew21.pydbus.tests.publish_async")

	def callback(x, returned=None, error=None):
		print("asyn: " + returned)
		assert (returned is not None)
		assert(error is None)
		assert(x == int(returned.split()[1]))

		global done
		done += 1
		if done == 3:
			loop.quit()

	def t1_func():
		remote.HelloWorld(1, callback=callback, callback_args=(1,))
		remote.HelloWorld(2, callback=callback, callback_args=(2,))
		print("sync: " + remote.HelloWorld(3))
		remote.HelloWorld(4, callback=callback, callback_args=(4,))

	t1 = Thread(None, t1_func)
	t1.daemon = True

	def handle_timeout():
		print("ERROR: Timeout.")
		sys.exit(1)

	GLib.timeout_add_seconds(2, handle_timeout)

	t1.start()

	loop.run()

	t1.join()
