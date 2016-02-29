from gi.repository import GLib, Gio

class MethodCallFunc:
	__slots__ = ["object", "outargs"]

	def __init__(self, object, node_info):
		self.object = object

		self.outargs = {}
		for iface in node_info.interfaces:
			for method in iface.methods:
				self.outargs[iface.name + "." + method.name] = [arg.signature for arg in method.out_args]

	def __call__(self, connection, sender, object_path, interface_name, method_name, parameters, invocation):
		try:
			outargs = self.outargs[interface_name + "." + method_name]
			soutargs = "(" + "".join(outargs) + ")"

			method = getattr(self.object, method_name)

			result = method(*parameters)

			#if len(outargs) == 1:
			#	result = (result,)

			if len(outargs) == 0:
				invocation.return_value(None)
			else:
				invocation.return_value(GLib.Variant(soutargs, result))

		except Exception as e:
			#TODO Think of a better way to translate Python exception types to DBus error types.
			e_type = type(e).__name__
			if not "." in e_type:
				e_type = "unknown." + e_type
			invocation.return_dbus_error(e_type, str(e))

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

		return ObjectRegistration(self.con, path, interface, MethodCallFunc(object, node_info), None, None)
