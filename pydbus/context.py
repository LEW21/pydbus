def CompositeContextManagerClass(free_method_name):
	class CompositeContextManager(object):
		__slots__ = ("submanagers")

		def __init__(self, *submanagers):
			self.submanagers = submanagers

		def __enter__(self):
			for sub in self.submanagers:
				sub.__enter__()

			return self

		def __exit__(self, exc_type, exc_value, traceback):
			for sub in reversed(self.submanagers):
				sub.__exit__(exc_type, exc_value, traceback)

			self.submanagers = None

	def free(self):
		self.__exit__(None, None, None)

	setattr(CompositeContextManager, free_method_name, free)

	return CompositeContextManager
