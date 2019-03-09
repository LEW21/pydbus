from pydbus import SessionBus
from gi.repository import GLib
from threading import Thread
import sys
import os

loop = GLib.MainLoop()


with open(__file__) as f:
	contents = f.read()


class TestObject(object):
	"""
	<node>
	<interface name="baz.bar.Foo">
		<method name="Hello">
			<arg type="h" name="in_fd" direction="in"/>
			<arg type="h" name="out_fd" direction="out"/>
		</method>
	</interface>
	</node>
	"""
	def Hello(self, in_fd):
		with os.fdopen(in_fd) as in_file:
			in_file.seek(0)
			assert(contents == in_file.read())
			print("Received fd as in parameter ok")
		with open(__file__) as out_file:
			assert(contents == out_file.read())
			return os.dup(out_file.fileno())

bus = SessionBus()


with bus.publish("baz.bar.Foo", TestObject()):
	remote = bus.get("baz.bar.Foo")

	def thread_func():
		with open(__file__) as in_file:
			assert(contents == in_file.read())
			out_fd = remote.Hello(in_file.fileno())
			with os.fdopen(out_fd) as out_file:
				out_file.seek(0)
				assert(contents == out_file.read())
				print("Received fd as out argument ok")
		loop.quit()

	thread = Thread(target=thread_func)
	thread.daemon = True

	def handle_timeout():
		exit("ERROR: Timeout.")

	GLib.timeout_add_seconds(2, handle_timeout)

	thread.start()
	loop.run()
	thread.join()
