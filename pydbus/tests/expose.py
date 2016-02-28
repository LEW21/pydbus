from pydbus import SessionBus
from gi.repository import GObject

class TestObject:
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
		print(res)
		return res

with SessionBus() as bus:
	with bus.expose("net.lew21.pydbus.Test", TestObject("Main"), ("Lol", TestObject("Lol"))):
		remoteMain = bus.get("net.lew21.pydbus.Test")
		remoteLol = bus.get("net.lew21.pydbus.Test", "Lol")

		# TODO run remoteMain.HelloWorld() and remoteLol.HelloWorld() in another thread.

		GObject.MainLoop().run()
