import greenlet

class AsyncFunction(object):
	def __init__(self, sync, start, finish):
		self.sync = sync
		self.start = start
		self.finish = finish

	def __call__(self, *args):
		my_greenlet = greenlet.getcurrent()

		if not my_greenlet.parent:
			return self.sync(*([arg for arg in args] + [None]))

		def cb(_, res):
			my_greenlet.switch(res)

		self.start(*([arg for arg in args] + [None, cb]))

		res = my_greenlet.parent.switch()

		return self.finish(res)

def spawn(func):
	greenlet.greenlet(func).switch()
