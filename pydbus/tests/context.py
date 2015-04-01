from pydbus import SessionBus

with SessionBus() as bus:
	notifications = bus.get('.Notifications')
	assert(notifications.Notify)

assert(bus.con is None)

with SessionBus() as bus:
	notifications = bus.get('.Notifications')
	assert(notifications.Notify)

assert(bus.con is None)
