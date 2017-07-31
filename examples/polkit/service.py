import logging

from gi.repository import GLib

from pydbus import SystemBus


loop = GLib.MainLoop()

class TestObject(object):
	dbus = '''
<node>
	<interface name='net.lew21.pydbus.PolkitExample'>
		<method name='TestAuth'>
			<arg type='b' name='interactive' direction='in'/>
			<arg type='s' name='response' direction='out'/>
		</method>
	</interface>
</node>
	'''
	def TestAuth(self, interactive, dbus_context):
		if dbus_context.is_authorized('org.freedesktop.policykit.exec', {'polkit.icon': 'abcd', 'aaaa': 'zzzz'}, interactive=interactive):
			return "OK"
		else:
			return "Forbidden"

with SystemBus() as bus:
	with bus.publish("net.lew21.pydbus.PolkitExample", TestObject()):
		logging.info("Started.")
		loop.run()
