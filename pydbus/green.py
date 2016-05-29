try:
	from .green_greenlet import GreenFunc, sleep, spawn_in_green_thread
except ImportError:
	from .green_sync import GreenFunc, sleep, spawn_in_green_thread
