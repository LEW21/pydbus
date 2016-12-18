"""Automatic XML documentation generator."""
import inspect
import sys

from itertools import islice
from xml.etree import ElementTree

from pydbus.generic import signal


PROPERTY_EMITS_SIGNAL = "org.freedesktop.DBus.Property.EmitsChangedSignal"


# Python 2 treats them as methods, Python 3 as functions
ismethod = inspect.ismethod if sys.version_info[0] == 2 else inspect.isfunction


def extract_membered_types(function, require_strong_typing, arg_count):
	has_arg_types = hasattr(function, "arg_types")
	if has_arg_types:
		arg_types = function.arg_types
	elif require_strong_typing:
		raise ValueError(
			"No argument types defined for method "
			"'{}'".format(function.__name__))
	else:
		arg_types = (None, ) * arg_count

	if hasattr(function, "ret_type"):
		if not has_arg_types:
			raise ValueError(
				"Only explicit return type defined but no explicit "
				"argument types for method '{}'".format(function.__name__))
		ret_type = function.ret_type
	elif has_arg_types:
		raise ValueError(
			"Only explicit argument types defined but no explicit return "
			"for method '{}'".format(function.__name__))
	else:
		ret_type = None

	return arg_types, ret_type


def get_arguments_getargspec(function, require_strong_typing):
	"""Verify arguments using the getargspec function."""
	args, vargs, kwargs, defaults = inspect.getargspec(function)
	# Do not include 'dbus_*' parameters which have a special meaning
	args = [a for a in args[1:] if not a.startswith("dbus_")]
	arg_types, ret_type = extract_membered_types(
		function, require_strong_typing, len(args))

	if defaults is not None:
		raise ValueError(
			"Default values are not allowed for method "
			"'{}'".format(function.__name__))
	if vargs is not None or kwargs is not None:
		raise ValueError(
			"Variable arguments arguments are not allowed for method "
			"'{}'".format(function.__name__))
	return args, arg_types, ret_type


def get_arguments_signature(function, require_strong_typing):
	"""Verify arguments using the Signature class in Python 3."""
	signature = inspect.signature(function)
	# For whatever reason OrderedDict does not actually support slicing
	# Also do not include 'dbus_*' parameters which have a special meaning
	parameters = [
		p for p in islice(signature.parameters.values(), 1, None)
		if not p.name.startswith("dbus_")]
	if not all(param.default is param.empty for param in parameters):
		raise ValueError(
			"Default values are not allowed for method "
			"'{}'".format(function.__name__))
	if not all(param.kind == param.POSITIONAL_OR_KEYWORD
			for param in parameters):
		raise ValueError(
			"Variable arguments or keyword only arguments are not allowed for "
			"method '{}'".format(function.__name__))

	names = [p.name for p in parameters]
	arg_types = [
		param.annotation for param in parameters
		if param.annotation is not param.empty]
	if arg_types and hasattr(function, "arg_types"):
		raise ValueError(
			"Annotations and explicit argument types are used together in "
			"method '{}'".format(function.__name__))

	ret_type = signature.return_annotation
	if (ret_type is not signature.empty and
			hasattr(function, "ret_type")):
		raise ValueError(
			"Annotations and explicit return type are used together in "
			"method '{}'".format(function.__name__))

	# Fall back to the explicit types only if there were no annotations, but
	# that might be actually valid if the function returns nothing and has
	# no parameters.
	# So it also checks that the function has any parameter or it has either of
	# the two attributes defined.
	# So it won't actually raise an error if a function has no parameter and
	# no annotations and no explicit types defined, because it is not possible
	# to determine if a function returns something.
	if (ret_type is signature.empty and not arg_types and
			(parameters or hasattr(function, "arg_types") or
				hasattr(function, "ret_type"))):
		arg_types, ret_type = extract_membered_types(
			function, require_strong_typing, len(parameters))

	if ret_type is signature.empty:
		# Instead of 'empty' we use None as each type should be strings
		ret_type = None

	return names, arg_types, ret_type


def get_arguments(function, require_strong_typing=False):
	"""Verify that the function is correctly defined."""
	if sys.version_info[0] == 2:
		verify_func = get_arguments_getargspec
	else:
		verify_func = get_arguments_signature

	names, arg_types, ret_type = verify_func(function, require_strong_typing)
	if len(arg_types) != len(names):
		raise ValueError(
			"Number of argument types ({}) differs from the number of "
			"parameters ({}) in function '{}'".format(
				len(arg_types), len(names), function.__name__))

	arg_types = tuple(zip(names, arg_types))

	return arg_types, ret_type


def generate_introspection_xml(cls, require_strong_typing=False):
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
		for arg, arg_type in arg_types:
			attrib = dict(base_attributes, name=arg)
			if arg_type is not None:
				attrib["type"] = arg_type
			ElementTree.SubElement(entry, "arg", attrib)


	interfaces = {}
	root = ElementTree.Element("node")
	for name, value in inspect.getmembers(cls, predicate=valid_member):
		entry = None  # in case something gets through
		attributes = {"name": name}
		if isinstance(value, property):
			entry = ElementTree.SubElement(
				get_interface(value.fget), "property")
			if sys.version_info[0] == 3:
				signature = inspect.signature(value.fget)
				prop_type = signature.return_annotation
				if prop_type is signature.empty:
					prop_type = None
				elif hasattr(function, "prop_type"):
					raise ValueError(
						"Annotations and explicit return type are used "
						"together in method '{}'".format(function.__name__))
			else:
				prop_type = None
			if prop_type is None and hasattr(value.fget, "prop_type"):
				prop_type = value.fget.prop_type

			if prop_type is not None:
				attributes["type"] = prop_type
			elif require_strong_typing:
				raise ValueError(
					"No type defined for property '{}'".format(name))

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
				arg_types, ret_type = get_arguments(
					value.method, require_strong_typing)
				if ret_type is not None:
					raise ValueError(
						"Return type defined for signal "
						"'{}'".format(value.method.__name__))
			elif require_strong_typing:
				raise ValueError(
					"No argument definitions for signal "
					"'{}'".format(value.method.__name__))
			else:
				arg_types = tuple()

			entry = ElementTree.SubElement(get_interface(value), "signal")
			add_arguments()
		elif ismethod(value):
			arg_types, ret_type = get_arguments(value, require_strong_typing)
			entry = ElementTree.SubElement(get_interface(value), "method")
			add_arguments(direction="in")
			if ret_type is not None:
				ElementTree.SubElement(
					entry, "arg",
					{"name": "return", "direction": "out", "type": ret_type})

		entry.attrib = attributes
	return ElementTree.tostring(root)


def attach_introspection_xml(cls):
	"""
	Generate and add introspection data to the class and return it.

	If used as a decorator without a parameter it won't require strong typing.
	If the parameter is True or False, it'll require it depending ot it.
	"""
	def decorate(cls):
		cls.dbus = generate_introspection_xml(cls, require_strong_typing)
		return cls
	if cls is True or cls is False:
		require_strong_typing = cls
		return decorate
	else:
		require_strong_typing = False
		return decorate(cls)


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
