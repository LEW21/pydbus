import time

from threading import Thread, Lock


class TimeLock(object):

	"""Lock which can timeout."""

	def __init__(self):
		self._lock = Lock()

	def acquire(self, blocking=True, timeout=-1):
		if timeout < 0:
			return self._lock.acquire(blocking)

		end_time = time.time() + timeout
		while time.time() < end_time:
			if self._lock.acquire(False):
				return True
			else:
				time.sleep(0.001)
		return False

	def release(self):
		return self._lock.release()

	def __enter__(self):
		self.acquire()

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.release()


class ClientPool(object):

	"""A pool of threads, which determines if every thread finished."""

	def __init__(self, finisher):
		self._threads = set()
		self._finisher = finisher
		self._lock = Lock()

	def add(self, thread):
		if thread in self._threads:
			raise ValueError('Thread was already added')
		self._threads.add(thread)

	def finish(self, thread):
		with self._lock:
			self._threads.remove(thread)
			finished = not self._threads

		if finished:
			self._finisher()


class ClientThread(Thread):

	"""
	Thread subclass which is also handling the main loop.

	Each thread can be a part of a pool. If every thread of the pool has
	finished, it'll execute some finishing action (usually to quit the loop).
	If no pool is defined, it'll make the thread part of it's own pool.

	The return value of the function is saved as the result. If the function
	raised an `AssertionError` it'll save that exception. In any case it'll
	tell the pool that it finished.
	"""

	def __init__(self, func, loop, pool=None):
		super(ClientThread, self).__init__(None)
		self.daemon = True
		self.loop = loop
		self.func = func
		self._lock = TimeLock()
		self._result = None
		if pool is None:
			pool = ClientPool(loop.quit)
		self._pool = pool
		if pool is not False:
			self._pool.add(self)

	def run(self):
		with self._lock:
			while not self.loop.is_running:
				pass
			try:
				self._result = self.func()
			except AssertionError as e:
				self._result = e
			finally:
				if self._pool is not False:
					self._pool.finish(self)

	@property
	def result(self):
		# If the thread itself quit the loop, it might not have released the
		# lock before the main thread already continues to get the result. So
		# wait for a bit to actually let the thread finish.
		if self._lock.acquire(timeout=0.1):
			try:
				if isinstance(self._result, AssertionError):
					# This will say the error happened here, even though it
					# happened inside the thread.
					raise self._result
				else:
					return self._result
			finally:
				self._lock.release()
		else:
			raise ValueError()
