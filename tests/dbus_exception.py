from pydbus import SessionBus, DBusException
from gi.repository import GLib
from threading import Thread
import sys

done = 0
loop = GLib.MainLoop()

class CustomDBusException(DBusException):
	dbus_name = "net.lew21.pydbus.Test.Error.Custom"
	silent = True

class TestObject(object):
	'''
<node>
	<interface name='net.lvht.ExceptionTest'>
		<method name='QuitService'>
		</method>
		<method name='RaiseException'>
		</method>
		<method name='RaiseDBusException'>
		</method>
	</interface>
</node>
	'''
	def __init__(self, id):
		self.id = id

	def QuitService(self):
		loop.quit()
		return None

	def RaiseException(self):
		raise Exception("sensitive")
		return None

	def RaiseDBusException(self):
		raise CustomDBusException("insensitive")
		return None


bus = SessionBus()

with bus.publish("net.lew21.pydbus.Test", TestObject("Main")):
	remoteMain = bus.get("net.lew21.pydbus.Test")

	def t1_func():
		try:
			remoteMain.RaiseDBusException()
		except Exception as e:
			if 'insensitive' not in str(e):
				raise e
			if CustomDBusException.dbus_name not in str(e):
				raise e
		try:
			remoteMain.RaiseException()
		except Exception as e:
			if 'sensitive' in str(e):
				raise e
			if DBusException.dbus_name not in str(e):
				raise e
		remoteMain.QuitService()

	t1 = Thread(None, t1_func)
	t1.daemon = True

	def handle_timeout():
		print("ERROR: Timeout.")
		sys.exit(1)

	GLib.timeout_add_seconds(2, handle_timeout)

	t1.start()

	loop.run()

	t1.join()
