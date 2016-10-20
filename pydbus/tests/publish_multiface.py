from pydbus import SessionBus
from gi.repository import GLib
from threading import Thread, Lock
import sys
import time

import pytest

from pydbus.tests.util import ClientThread

class DummyObject(object):
	'''
<node>
	<interface name='net.lew21.pydbus.tests.Iface1'>
		<method name='Method1'>
			<arg type='s' name='response' direction='out'/>
		</method>
	</interface>
	<interface name='net.lew21.pydbus.tests.Iface2'>
		<method name='Method2'>
			<arg type='s' name='response' direction='out'/>
		</method>
	</interface>
</node>
	'''

	def __init__(self):
		self.done = []

	def Method1(self):
		self.done += ["Method1"]
		return self.done[-1]

	def Method2(self):
		self.done += ["Method2"]
		return self.done[-1]


@pytest.fixture
def defaults():
	loop = GLib.MainLoop()
	loop.cancelled = False
	bus = SessionBus()

	obj = DummyObject()
	with bus.publish("net.lew21.pydbus.tests.expose_multiface", obj):
		yield loop, obj, bus.get("net.lew21.pydbus.tests.expose_multiface")


def run(loop, func):
	thread = ClientThread(func, loop)
	GLib.timeout_add_seconds(2, loop.quit)

	thread.start()
	loop.run()

	try:
		return thread.result
	except ValueError:
		pytest.fail('Unable to finish thread')


def test_using_multiface(defaults):
	def thread_func():
		results = []
		results += [remote.Method1()]
		results += [remote.Method2()]
		return results

	loop, obj, remote = defaults

	result = run(loop, thread_func)

	assert result == ["Method1", "Method2"]
	assert obj.done == ["Method1", "Method2"]


@pytest.mark.parametrize("interface, method", [
	("net.lew21.pydbus.tests.Iface1", "Method1"),
	("net.lew21.pydbus.tests.Iface2", "Method2"),
])
def test_using_specific_interface(defaults, interface, method):
	def thread_func():
		return getattr(remote, method)()

	loop, obj, remote = defaults
	remote = remote[interface]

	result = run(loop, thread_func)

	assert result == method
	assert obj.done == [method]


@pytest.mark.parametrize("interface, method", [
	("net.lew21.pydbus.tests.Iface1", "Method2"),
	("net.lew21.pydbus.tests.Iface2", "Method1"),
])
def test_using_wrong_interface(defaults, interface, method):
	def thread_func():
		with pytest.raises(AttributeError) as e:
			getattr(remote, method)()
		return e

	loop, obj, remote = defaults
	remote = remote[interface]

	result = run(loop, thread_func)

	assert str(result.value) == "'{}' object has no attribute '{}'".format(
		interface, method)
	assert obj.done == []
