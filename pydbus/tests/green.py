from pydbus import SessionBus
from gi.repository import GLib

import greenlet

loop = GLib.MainLoop()

def myfunc():
	try:
		with SessionBus() as bus:
			print(bus.dbus)
	finally:
		loop.quit()

g = greenlet.greenlet(myfunc)
g.switch()
loop.run()

with SessionBus() as bus:
	print(bus.dbus)
