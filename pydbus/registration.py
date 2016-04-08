from gi.repository import Gio

def MethodCallFunc(object):
	def method_call_callback(connection, sender, object_path, interface_name, method_name, parameters, invocation):
		# TODO
		...

	return method_call_callback

class ObjectRegistration(object):
	__slots__ = ("con", "id")

	def __init__(self, con, path, interface, method_call_callback, get_property_callback, set_property_callback):
		self.con = con
		self.id = con.register_object(path, interface, method_call_callback, get_property_callback, set_property_callback)

	def unregister(self):
		self.con.unregister_object(self.id)
		self.con = None
		self.id = None

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if not self.id is None:
			self.unregister()

class RegistrationMixin:
	__slots__ = ()

	def register_object(self, path, object, node_info):
		if node_info is None:
			try:
				node_info = type(object).dbus
			except AttributeError:
				node_info = type(object).__doc__

		node_info = Gio.DBusNodeInfo.new_for_xml(node_info)

		if len(node_info.interfaces) > 1:
			raise NotImplementedError("Support for multiple interfaces is not implemented.")

		interface = node_info.interfaces[0]

		return ObjectRegistration(self.con, path, interface, MethodCallFunc(object), None, None)
