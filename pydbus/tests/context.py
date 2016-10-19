from pydbus import SessionBus, connect
import os

import pytest


def test_remove_dbus():
	DBUS_SESSION_BUS_ADDRESS = os.getenv("DBUS_SESSION_BUS_ADDRESS")

	with connect(DBUS_SESSION_BUS_ADDRESS) as bus:
		bus.dbus

	del bus._dbus
	with pytest.raises(RuntimeError):
		bus.dbus


def test_use_exited_bus():
	"""Test using a bus instance after its context manager."""
	with SessionBus() as bus:
		pass

	# SessionBus() and SystemBus() are not closed automatically, so this should work:
	bus.dbus

	with bus.request_name("net.lew21.Test"):
		pass

	with bus.request_name("net.lew21.Test"):
		pass

	with bus.request_name("net.lew21.Test"):
		with pytest.raises(RuntimeError):
			bus.request_name("net.lew21.Test")

	with bus.watch_name("net.lew21.Test"):
		pass

	with bus.subscribe(sender="net.lew21.Test"):
		pass
