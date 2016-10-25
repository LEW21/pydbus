"""Automatic XML documentation generator."""
import inspect
import sys

from xml.etree import ElementTree

from pydbus.generic import signal


PROPERTY_EMITS_SIGNAL = "org.freedesktop.DBus.Property.EmitsChangedSignal"


# Python 2 treats them as methods, Python 3 as functions
ismethod = inspect.ismethod if sys.version_info[0] == 2 else inspect.isfunction


def get_arguments(function):
	"""Verify that the function is correctly defined."""
	args, vargs, kwargs, defaults = inspect.getargspec(function)
	# Do not include 'dbus_*' parameters which have a special meaning
	args = [a for a in args[1:] if not a.startswith("dbus_")]
	if defaults is not None:
		raise ValueError(
			"Default values are not allowed for method "
			"'{}'".format(function.__name__))
	if vargs is not None or kwargs is not None:
		raise ValueError(
			"Variable arguments arguments are not allowed for method "
			"'{}'".format(function.__name__))
	return args


def generate_introspection_xml(cls):
	"""Generate introspection XML for the given class."""
	def get_interface(entry):
		"""Get the interface XML element for the given member."""
		if getattr(entry, "dbus_interface", None) is None:
			interface = cls.dbus_interface
			if interface is None:
				raise ValueError(
					"No interface defined for '{}'".format(entry.__name__))
		else:
			interface = entry.dbus_interface
		if interface not in interfaces:
			interfaces[interface] = ElementTree.SubElement(
				root, "interface", {"name": interface})
		return interfaces[interface]

	def valid_member(member):
		"""Only select members with the correct type and name."""
		if isinstance(member, property):
			member = member.fget
		elif not ismethod(member) and not isinstance(member, signal):
			return False
		return member.__name__[0].isupper()

	def add_arguments(**base_attributes):
		for arg in args:
			attrib = dict(base_attributes, name=arg)
			ElementTree.SubElement(entry, "arg", attrib)


	interfaces = {}
	root = ElementTree.Element("node")
	for name, value in inspect.getmembers(cls, predicate=valid_member):
		entry = None  # in case something gets through
		attributes = {"name": name}
		if isinstance(value, property):
			entry = ElementTree.SubElement(
				get_interface(value.fget), "property")
			if value.fset is None:
				attributes["access"] = "read"
			else:
				attributes["access"] = "readwrite"
			if getattr(value.fget, "causes_signal", False) is True:
				ElementTree.SubElement(
					entry, "annotation",
					{"name": PROPERTY_EMITS_SIGNAL, "value": "true"})
		elif isinstance(value, signal):
			if hasattr(value, "method"):
				args = get_arguments(value.method)
			else:
				args = tuple()

			entry = ElementTree.SubElement(get_interface(value), "signal")
			add_arguments()
		elif ismethod(value):
			args = get_arguments(value)
			entry = ElementTree.SubElement(get_interface(value), "method")
			add_arguments(direction="in")

		entry.attrib = attributes
	return ElementTree.tostring(root)


def attach_introspection_xml(cls):
	"""Generate and add introspection data to the class and return it."""
	cls.dbus = generate_introspection_xml(cls)
	return cls


def emits_changed_signal(prop):
	"""Decorate a property to emit a changing signal."""
	prop.fget.causes_signal = True
	return prop


def interface(name):
	"""Define an interface for a method, property or class."""
	def decorate(obj):
		obj.dbus_interface = name
		return obj
	return decorate
