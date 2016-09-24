try:
	from .green_greenlet import GreenFunc, spawn_in_green_thread
except ImportError:
	from .green_sync import GreenFunc, spawn_in_green_thread

from gi.repository import GLib

def sleep_start(seconds, cb):
	def sleep_cb():
		cb(None, None)
		return False

	GLib.timeout_add(seconds * 1000, sleep_cb)

sleep_finish = (lambda x: x)

from time import sleep as sleep_sync

sleep = GreenFunc(sleep_start, sleep_finish, sleep_sync)
