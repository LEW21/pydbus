from gi.repository import Gio, GLib
import gevent.threadpool
import gevent.event
from . import autostart_glib

class AsyncFunction(object):
	def __init__(self, sync, start, finish):
		self.sync = sync
		self.start = start
		self.finish = finish

	def __call__(self, *args):
		autostart_glib()
		#if not glib_service_started:
		#	return self.sync(*([arg for arg in args] + [None]))

		cancellable = Gio.Cancellable.new()
		res = gevent.event.AsyncResult()
		safe_res = gevent.threadpool.ThreadResult(res)

		def cb(_, cbres):
			safe_res.set(cbres)

		def start_fn():
			self.start(*([arg for arg in args] + [cancellable, cb]))
		GLib.idle_add(start_fn)

		try:
			received_res = res.get()
		except:
			cancellable.cancel()
			raise

		return self.finish(received_res)
