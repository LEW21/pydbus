#!/usr/bin/env python

from gi.repository import GLib

from pydbus import SessionBus
from pydbus.generic import signal

'''  commands to exercise this:
dbus-send --session --type=method_call  --print-reply --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.GetServerInformation

gdbus call --session  --dest org.freedesktop.Notifications --object-path /org/freedesktop/Notifications --method org.freedesktop.Notifications.Notify 'myapp' 4 "icon" "summary" "body"  "[ 'app1', 'app2' ]"  "{ 'hint1':<'hintinfo'> }" 3

dbus-send --session --type=method_call  --print-reply --dest=org.freedesktop.Notifications /org/freedesktop/Notifications org.freedesktop.Notifications.GetCapabilities
'''

class Notifications(object):
	"""
	<node>
		<interface name="org.freedesktop.Notifications">
			<signal name="NotificationClosed">
				<arg direction="out" type="u" name="id"/>
				<arg direction="out" type="u" name="reason"/>
			</signal>
			<signal name="ActionInvoked">
				<arg direction="out" type="u" name="id"/>
				<arg direction="out" type="s" name="action_key"/>
			</signal>
			<method name="Notify">
				<arg direction="out" type="u"/>
				<arg direction="in" type="s" name="app_name"/>
				<arg direction="in" type="u" name="replaces_id"/>
				<arg direction="in" type="s" name="app_icon"/>
				<arg direction="in" type="s" name="summary"/>
				<arg direction="in" type="s" name="body"/>
				<arg direction="in" type="as" name="actions"/>
				<arg direction="in" type="a{sv}" name="hints"/>
				<arg direction="in" type="i" name="timeout"/>
			</method>
			<method name="CloseNotification">
				<arg direction="in" type="u" name="id"/>
			</method>
			<method name="GetCapabilities">
				<arg direction="out" type="as" name="caps"/>
			</method>
			<method name="GetServerInformation">
				<arg direction="out" type="s" name="name"/>
				<arg direction="out" type="s" name="vendor"/>
				<arg direction="out" type="s" name="version"/>
				<arg direction="out" type="s" name="spec_version"/>
			</method>
		</interface>
	</node>
	"""

	NotificationClosed = signal()
	ActionInvoked = signal()

	def Notify(self, app_name, replaces_id, app_icon, summary, body, actions, hints, timeout):
		print("Notification: {} {} {} {} {} {} {} {}".format(app_name, replaces_id, app_icon, summary, body, actions, hints, timeout))
		return 4 # chosen by fair dice roll. guaranteed to be random.

	def CloseNotification(self, iid):
		pass

	def GetCapabilities(self):
		return []

	def GetServerInformation(self):
		return ("pydbus.examples.notifications_server", "pydbus", "?", "1.1")

bus = SessionBus()
bus.publish("org.freedesktop.Notifications", Notifications())
loop = GLib.MainLoop()
loop.run()
