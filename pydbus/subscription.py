from gi.repository import Gio

class Subscription(object):
	Flags = Gio.DBusSignalFlags
	__slots__ = ("con", "id")

	def __init__(self, con, sender, iface, member, object, arg0, flags, callback):
		self.con = con
		self.id = con.signal_subscribe(sender, iface, member, object, arg0, flags, callback)

	def unsubscribe(self):
		self.con.signal_unsubscribe(self.id)
		self.con = None
		self.id = None

	def disconnect(self):
		"""An alias for unsubscribe()"""
		self.unsubscribe()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if not self.id is None:
			self.unsubscribe()

class SubscriptionMixin(object):
	__slots__ = ()
	SubscriptionFlags = Subscription.Flags

	def subscribe(self, sender=None, iface=None, signal=None, object=None, arg0=None, flags=0, signal_fired=None):
		"""Subscribes to matching signals.

		Subscribes to signals on connection and invokes signal_fired callback
		whenever the signal is received.

		To receive signal_fired callback, you need GLib main loop.
		You can execute it with GObject.MainLoop().run().

		Parameters
		----------
		sender : string, optional
			Sender name to match on (unique or well-known name) or None to listen from all senders.
		iface : string, optional
			Interface name to match on or None to match on all interfaces.
		signal : string, optional
			Signal name to match on or None to match on all signals.
		object : string, optional
			Object path to match on or None to match on all object paths.
		arg0 : string, optional
			Contents of first string argument to match on or None to match on all kinds of arguments.
		flags : SubscriptionFlags, optional
		signal_fired : callable, optional
			Invoked when there is a signal matching the requested data.
			Parameters: sender, object, iface, signal, params

		Returns
		-------
		Subscription
			An object you can use as a context manager to unsubscribe from the signal later.

		See Also
		--------
		See https://developer.gnome.org/gio/2.44/GDBusConnection.html#g-dbus-connection-signal-subscribe
		for more information.
		"""
		callback = (lambda con, sender, object, iface, signal, params: signal_fired(sender, object, iface, signal, params.unpack())) if signal_fired is not None else lambda *args: None
		return Subscription(self.con, sender, iface, signal, object, arg0, flags, callback)
