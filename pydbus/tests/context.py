from pydbus import SessionBus

with SessionBus() as bus:
	assert(bus.dbus.RequestName)

assert(bus.con is None)

with SessionBus() as bus:
	assert(bus.dbus.RequestName)

assert(bus.con is None)

with SessionBus() as bus:

	with bus.request_name("net.lew21.Test"):
		pass

	with bus.request_name("net.lew21.Test"):
		pass

	with bus.request_name("net.lew21.Test"):
		try:
			bus.request_name("net.lew21.Test")
			assert(False)
		except RuntimeError:
			pass

	with bus.watch_name("net.lew21.Test"):
		pass

	with bus.subscribe(sender="net.lew21.Test"):
		pass
