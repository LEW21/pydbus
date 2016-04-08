#!/usr/bin/env python

# Based on http://stackoverflow.com/questions/22390064/use-dbus-to-just-send-a-message-in-python

# Python DBUS Test Server
# runs until the Quit() method is called via DBUS

from gi.repository import GObject
from pydbus import SessionBus

loop = GObject.MainLoop()

class MyDBUSService(object):
	"""
		<node>
			<interface name='net.lew21.pydbus.ClientServerExample'>
				<method name='Hello'>
					<arg type='s' name='response' direction='out'/>
				</method>
				<method name='EchoString'>
					<arg type='s' name='a' direction='in'/>
					<arg type='s' name='response' direction='out'/>
				</method>
				<method name='Quit'/>
			</interface>
		</node>
	"""

	def Hello(self):
		"""returns the string 'Hello, World!'"""
		return "Hello, World!"

	def EchoString(self, s):
		"""returns whatever is passed to it"""
		return s

	def Quit(self):
		"""removes this object from the DBUS connection and exits"""
		loop.quit()

bus = SessionBus()
bus.publish("net.lew21.pydbus.ClientServerExample", MyDBUSService())
loop.run()
