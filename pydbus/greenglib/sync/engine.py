def AsyncFunction(sync, start, finish):
	return lambda *args: sync(*([arg for arg in args] + [None]))

def spawn(func):
	func()
