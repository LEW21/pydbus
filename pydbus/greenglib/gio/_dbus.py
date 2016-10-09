from gi.repository import Gio
from functools import wraps
from .._engine import AsyncFunction, Spawner, GreenProperty
from ..glib._variant import upcast as upcast_variant

def bus_get(bus_type):
	bus = AsyncFunction(Gio.bus_get_sync, Gio.bus_get, Gio.bus_get_finish)(bus_type)
	return bus.green

# Nothing for g_bus_(un)own_name, because g_bus_unown_name works synchroneously.
# It's simply broken.

def bus_watch_name_on_connection(con, name, flags, name_appeared_handler, name_vanished_handler):
	return Gio.bus_watch_name_on_connection(con.pygi, name, flags, Spawner(name_appeared_handler), Spawner(name_vanished_handler))

def bus_unwatch_name(id):
	return Gio.bus_unwatch_name(id)

class DBusConnection(object):
	"""
	We're automatically thread-safe, because:

	As an exception to the usual GLib rule that a particular object must not be used by two threads at the same time, GDBusConnection's methods may be called from any thread. This is so that g_bus_get() and g_bus_get_sync() can safely return the same GDBusConnection when called from any thread.
	"""
	def __init__(self, pygi):
		self.pygi = pygi

	def call(self, bus_name, object_path, interface_name, method_name, parameters, reply_type, flags, timeout_msec):
		f = AsyncFunction(self.pygi.call_sync, self.pygi.call, self.pygi.call_finish)
		return upcast_variant(f(bus_name, object_path, interface_name, method_name, parameters, reply_type, flags, timeout_msec))

	def signal_subscribe(self, sender, interface_name, member, object_path, arg0, flags, callback):
		return self.pygi.signal_subscribe(sender, interface_name, member, object_path, arg0, flags, Spawner(callback))

	def signal_unsubscribe(self, subscription_id):
		return self.pygi.signal_unsubscribe(subscription_id)

	def register_object(self, object_path, interface_info, method_call_closure):
		"""
		get_property_closure and set_property_closure are not used, as they can't properly support greenlets.

		Gio docs: "Since 2.38, if you want to handle getting/setting D-Bus properties asynchronously, give NULL as your get_property() or set_property() function. The D-Bus call will be directed to your method_call function, with the provided interface_name set to "org.freedesktop.DBus.Properties"."
		"""
		return self.pygi.register_object(object_path, interface_info, Spawner(method_call_closure), None, None)

	def unregister_object(self, registration_id):
		return self.pygi.unregister_object(registration_id)

	def emit_signal(destination_bus_name, object_path, interface_name, signal_name, parameters):
		return self.pygi.emit_signal(destination_bus_name, object_path, interface_name, signal_name, parameters)

	watch_name = bus_watch_name_on_connection
	unwatch_name = staticmethod(bus_unwatch_name)

	@staticmethod
	def new(stream, guid, flags=0, observer=None):
		f = AsyncFunction(Gio.DBusConnection.new_sync, Gio.DBusConnection.new, Gio.DBusConnection.new_finish)
		return f(stream, guid, flags, observer).green

	@staticmethod
	def new_for_address(address, flags=0, observer=None):
		f = AsyncFunction(Gio.DBusConnection.new_for_address_sync, Gio.DBusConnection.new_for_address, Gio.DBusConnection.new_for_address_finish)
		return f(address, flags, observer).green

	def start_message_processing(self):
		self.pygi.start_message_processing()

	def close(self):
		f = AsyncFunction(self.pygi.close_sync, self.pygi.close, self.pygi.close_finish)
		return f()

Gio.DBusConnection.green = GreenProperty(DBusConnection)
