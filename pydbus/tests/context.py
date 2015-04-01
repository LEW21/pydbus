from pydbus import SessionBus

with SessionBus() as bus:
	notifications = bus.get('.Notifications')
	assert(notifications.Notify)

assert(bus.con is None)

with SessionBus() as bus:
	notifications = bus.get('.Notifications')
	assert(notifications.Notify)

assert(bus.con is None)

with SessionBus() as bus:

	with bus.own_name("net.lew21.Test"):
		pass

	with bus.watch_name("net.lew21.Test"):
		pass

	with bus.subscribe(sender="net.lew21.Test"):
		pass
