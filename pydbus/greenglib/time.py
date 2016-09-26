from __future__ import absolute_import

from . import AsyncFunction
from gi.repository import GLib

def sleep_start(seconds, cancellable, cb):
	def sleep_cb():
		cb(None, None)
		return False

	GLib.timeout_add(seconds * 1000, sleep_cb)

sleep_finish = (lambda x: x)

from time import sleep as sleep_sync_impl

def sleep_sync(seconds, cancellable):
	sleep_sync_impl(seconds)

sleep = AsyncFunction(sleep_sync, sleep_start, sleep_finish)
