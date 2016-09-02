from gi.repository import GLib
from xml.etree import ElementTree as ET
from .auto_names import *

from .proxy_method import ProxyMethod
from .proxy_property import ProxyProperty
from .proxy_signal import ProxySignal, OnSignal

from .green import GreenFunc

class ProxyMixin(object):
	__slots__ = ()

	def get(self, bus_name, object_path=None):
		"""Get a remote object.

		Parameters
		----------
		bus_name : string
			Name of the service that exposes this object.
			You may start with "." - then org.freedesktop will be automatically prepended.
		object_path : string, optional
			Path of the object. If not provided, bus_name translated to path format is used.

		Returns
		-------
		ProxyObject implementing all the Interfaces exposed by the remote object.
		Note that it inherits from multiple Interfaces, so the method you want to use
		may be shadowed by another one, eg. from a newer version of the interface.
		Therefore, to interact with only a single interface, use:
		>>> bus.get("org.freedesktop.systemd1")["org.freedesktop.systemd1.Manager"]
		or simply
		>>> bus.get(".systemd1")[".Manager"]
		which will give you access to the one specific interface.
		"""
		bus_name = auto_bus_name(bus_name)
		object_path = auto_object_path(bus_name, object_path)

		try:
			con = GreenFunc(self.con.call, self.con.call_finish, self.con.call_sync)
		except NotImplementedError:
			# We have an GLib < 2.46 use legacy support
			con = self.con.call_sync
		xml, = con(
			bus_name, object_path,
			'org.freedesktop.DBus.Introspectable', "Introspect", None, GLib.VariantType.new("(s)"),
			0, self.timeout, None).unpack()

		introspection = ET.fromstring(xml)

		if len(introspection) == 0:
			raise KeyError("no such object")

		return CompositeInterface(introspection)(self, bus_name, object_path)

class ProxyObject(object):
	def __init__(self, bus, bus_name, path):
		self._bus = bus
		self._bus_name = bus_name
		self._path = path

def Interface(iface):

	class interface(ProxyObject):
		@staticmethod
		def _Introspect():
			print(iface.attrib["name"] + ":")
			for member in iface:
				print("\t" + member.tag + " " + member.attrib["name"])
			print()

	interface.__qualname__ = interface.__name__ = iface.attrib["name"]
	interface.__module__ = "DBUS"

	for member in iface:
		member_name = member.attrib["name"]
		if member.tag == "method":
			setattr(interface, member_name, ProxyMethod(interface.__name__, member))
		elif member.tag == "property":
			setattr(interface, member_name, ProxyProperty(interface.__name__, member))
		elif member.tag == "signal":
			signal = ProxySignal(interface.__name__, member)
			setattr(interface, member_name, signal)
			setattr(interface, "on" + member_name, OnSignal(signal))

	return interface

def CompositeInterface(introspection):
	class CompositeObject(ProxyObject):
		def __getitem__(self, iface):
			if iface == "" or iface[0] == ".":
				iface = self._path.replace("/", ".")[1:] + iface
			matching_bases = [base for base in type(self).__bases__ if base.__name__ == iface]

			if len(matching_bases) == 0:
				raise KeyError(iface)
			assert(len(matching_bases) == 1)

			iface_class = matching_bases[0]
			return iface_class(self._bus, self._bus_name, self._path)

		@classmethod
		def _Introspect(cls):
			for iface in cls.__bases__:
				try:
					iface._Introspect()
				except:
					pass

	ifaces = sorted([x for x in introspection if x.tag == "interface"], key=lambda x: int(x.attrib["name"].startswith("org.freedesktop.DBus.")))
	CompositeObject.__bases__ = tuple(Interface(iface) for iface in ifaces)
	CompositeObject.__name__ = "<CompositeObject>"
	CompositeObject.__qualname__ = "<CompositeObject>(" + "+".join(x.__name__ for x in CompositeObject.__bases__) + ")"
	CompositeObject.__module__ = "DBUS"
	return CompositeObject
