import gevent.threadpool

class Queue:
	def __init__(self):
		self.mutex = gevent.threadpool.Lock()
		self.watcher = gevent.get_hub().loop.async()
		self.events = []

	def push(self, event):
		with self.mutex:
			self.events.append(event)
			self.watcher.send()

	def consume_available(self):
		return QueueConsumer(self)

	def consume(self):
		return GreenConsumer(self.consume_available(), gevent.get_hub().wait)

class QueueConsumer:
	def __init__(self, queue):
		self.queue = queue

	def __enter__(self):
		self.queue.mutex.acquire()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.queue.mutex.release()

	def start(self, *args):
		self.queue.watcher.start(*args)
		self.queue.mutex.release()

	def stop(self):
		self.queue.mutex.acquire()
		self.queue.watcher.stop()

	def __iter__(self):
		return self

	def __next__(self):
		if self.queue.events:
			return self.queue.events.pop(0)
		else:
			raise StopIteration

class GreenConsumer:
	def __init__(self, consumer, wait_fn):
		self.consumer = consumer
		self.wait_fn = wait_fn

	def __enter__(self):
		self.consumer.__enter__()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.consumer.__exit__(exc_type, exc_val, exc_tb)

	def __iter__(self):
		return self

	def __next__(self):
		try:
			return next(self.consumer)
		except StopIteration:
			self.wait_fn(self.consumer)
			return next(self.consumer)
