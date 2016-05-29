import time

def GreenFunc(start, finish, sync):
	return sync

sleep = time.sleep

def spawn_in_green_thread(func):
	return func
