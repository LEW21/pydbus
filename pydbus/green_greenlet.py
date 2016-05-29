import greenlet
from functools import wraps
from gi.repository import GLib
import time

class GreenFunc(object):
	def __init__(self, start, finish, sync):
		self.start = start
		self.finish = finish
		self.sync = sync

	def __call__(self, *args):
		my_greenlet = greenlet.getcurrent()

		if not my_greenlet.parent:
			return self.sync(*args)

		def cb(_, res):
			my_greenlet.switch(res)

		self.start(*args, cb)

		res = my_greenlet.parent.switch()

		return self.finish(res)

def sleep(seconds):
	my_greenlet = greenlet.getcurrent()

	if not my_greenlet.parent:
		time.sleep(seconds)
		return

	def cb():
		my_greenlet.switch()
		return False

	GLib.timeout_add(seconds * 1000, cb)
	my_greenlet.parent.switch()

def spawn_in_green_thread(func):
	@wraps(func)
	def callable(*args):
		call = greenlet.greenlet(func)
		call.switch(*args)
	return callable
