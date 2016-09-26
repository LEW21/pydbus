import sys
from functools import wraps

if sys.version_info < (3,0):
	# It's broken for functools.partial.
	wraps = lambda f: (lambda x: x)

def spawn(f):
	engine.spawn(f)

class AsyncFunction(object):
	def __init__(self, sync, start, finish):
		self.sync = sync
		self.start = start
		self.finish = finish

	def __call__(self, *args):
		return engine.AsyncFunction(self.sync, self.start, self.finish)(*args)

def Spawner(func):
	if func is None:
		return func

	@wraps(func)
	def callback(*args):
		spawn(lambda: func(*args))
	return callback

def GreenProperty(cls):
	def green(self):
		try:
			return self._green
		except AttributeError:
			self._green = cls(self)
			return self._green
	return property(green)



def _is_gevent_monkey_patched():
	if 'gevent.monkey' not in sys.modules:
		return False
	import gevent.socket
	import socket
	return socket.socket is gevent.socket.socket

if _is_gevent_monkey_patched():
	print("USING GEVENT")
	from .gevent import engine
else:
	try:
		from .greenlet import engine
		print("USING GREENLET")
	except ImportError:
		from .sync import engine
