from gi.repository import GLib


class ProxyProperty(object):
	def __init__(self, iface_name, iface_property):
		self._iface_name = iface_name
		self.__name__ = iface_property.attrib["name"]
		self.__qualname__ = self._iface_name + "." + self.__name__

		self._type = iface_property.attrib["type"]
		access = iface_property.attrib["access"]
		self._readable = access.startswith("read")
		self._writeable = access.endswith("write")
		self.__doc__ = "(" + self._type + ") " + access

	def __get__(self, instance, owner):
		if instance is None:
			return self

		if not self._readable:
			raise AttributeError("unreadable attribute")
		
		if instance._bus._ProxyMixin__translator:
			xlater = instance._translator
			v = instance._object["org.freedesktop.DBus.Properties"].Get(self._iface_name, self.__name__)
			return xlater.translate(
				pydevobject=instance,
				keyname=self.__name__,
				callerargs=v if isinstance(v, tuple) else (v,),
				calledby='property',
				fromDbusToPython=True,
				introspection=None,
				retained_pyarg=None)
		else:
			return instance._object["org.freedesktop.DBus.Properties"].Get(self._iface_name, self.__name__)

	def __set__(self, instance, value):
		if instance is None or not self._writeable:
			raise AttributeError("can't set attribute")

		if instance._translator:
			value = instance._translator.translate(
				pydevobject=instance,
				keyname=self.__name__,
				callerargs=value if isinstance(value, tuple) else (value,),
				calledby='property',
				fromDbusToPython=False,
				introspection=self._type,
				retained_pyarg=None)
		
		instance._object["org.freedesktop.DBus.Properties"].Set(self._iface_name, self.__name__, GLib.Variant(self._type, value))

	def __repr__(self):
		return "<property " + self.__qualname__ + " at 0x" + format(id(self), "x") + ">"
