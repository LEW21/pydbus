
class MethodCallContext(object):
	def __init__(self, bus, gdbus_method_invocation):
		self.bus = bus
		self._mi = gdbus_method_invocation

	@property
	def sender(self):
		return self._mi.get_sender()

	@property
	def object_path(self):
		return self._mi.get_object_path()

	@property
	def interface_name(self):
		return self._mi.get_interface_name()

	@property
	def method_name(self):
		return self._mi.get_method_name()
