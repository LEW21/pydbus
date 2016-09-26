from gi.repository import GLib
import gevent
import gevent.threadpool
from .spawn import dispatch

def glib_service():
	ctx = GLib.MainContext.default()
	ctx.acquire()
	loop = GLib.MainLoop()
	loop.run()

glib_service_started = False

def autostart_glib():
	global glib_service_started
	if glib_service_started:
		return
	glib_service_started = True

	pool = gevent.threadpool.ThreadPool(1)
	pool.spawn(glib_service)
	gevent.spawn(dispatch)
