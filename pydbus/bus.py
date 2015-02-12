from gi.repository import Gio, GLib
from xml.etree import ElementTree as ET

from .bus_names import OwnMixin, WatchMixin

class Bus(OwnMixin, WatchMixin):
	Type = Gio.BusType

	def __init__(self, type, timeout=10):
		self.con = Gio.bus_get_sync(type, None)
		self.timeout = timeout

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
		if bus_name[0] == ".":
			#Default namespace
			bus_name = "org.freedesktop" + bus_name

		if object_path is None:
			# They always name it like that.
			object_path = "/" + bus_name.replace(".", "/")

		xml = self.con.call_sync(
			bus_name, object_path,
			'org.freedesktop.DBus.Introspectable', "Introspect", None, GLib.VariantType.new("(s)"),
			0, self.timeout, None).unpack()[0]

		introspection = ET.fromstring(xml)

		return CompositeInterface(introspection)(self, bus_name, object_path)

	def close():
		self.con.close_sync(0)

def SystemBus():
	return Bus(Bus.Type.SYSTEM)

def SessionBus():
	return Bus(Bus.Type.SESSION)

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

	interface.__name__ = iface.attrib["name"]

	def Functor(method):
		iface_name = iface.attrib["name"]
		method_name = method.attrib["name"]
		inargs  = [arg.attrib["type"] for arg in method if arg.tag == "arg" and arg.attrib["direction"] == "in"]
		outargs = [arg.attrib["type"] for arg in method if arg.tag == "arg" and arg.attrib["direction"] == "out"]
		sinargs  = "(" + "".join(inargs) + ")"
		soutargs = "(" + "".join(outargs) + ")"
		def functor(self, *args):
			return self._bus.con.call_sync(
				self._bus_name, self._path,
				iface_name, method_name, GLib.Variant(sinargs, args), GLib.VariantType.new(soutargs),
				0, self._bus.timeout, None).unpack()
		functor.__name__ = method_name
		functor.__doc__ = "(" + ", ".join(inargs) + ")" + " -> " + "(" + ", ".join(outargs) + ")"
		return functor

	for member in iface:
		if member.tag == "method":
			setattr(interface, member.attrib["name"], Functor(member))

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

	CompositeObject.__bases__ = tuple(Interface(iface) for iface in introspection)
	return CompositeObject

if __name__ == "__main__":
	import sys
	title = sys.argv[1] if len(sys.argv) >= 2 else "Hello World!"
	message = sys.argv[2] if len(sys.argv) >= 3 else 'pydbus works :)'

	bus = SessionBus()
	notifications = bus.get('.Notifications') # org.freedesktop automatically prepended
	notifications[""].Notify('test', 0, 'dialog-information', title, message, [], {}, 5000)
	# [""] is not required, but makes us compatible with Gnome 2030.
