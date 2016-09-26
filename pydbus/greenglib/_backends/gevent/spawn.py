from .queue import Queue
import gevent

q = Queue()

def dispatch():
	with q.consume() as c:
		for ev in c:
			gevent.spawn(ev)

def spawn(func):
	q.push(func)
