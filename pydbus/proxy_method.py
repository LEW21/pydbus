from gi.repository import GLib
from .generic import bound_method

try:
	from inspect import Signature, Parameter
	put_signature_in_doc = False
except:
	from ._inspect3 import Signature, Parameter
	put_signature_in_doc = True

class DBUSSignature(Signature):

	def __str__(self):
		result = []
		for param in self.parameters.values():
			p = param.name if not param.name.startswith("arg") else ""
			if type(param.annotation) == str:
				p += ":" + param.annotation
			result.append(p)

		rendered = '({})'.format(', '.join(result))

		if self.return_annotation is not Signature.empty:
			rendered += ' -> {}'.format(self.return_annotation)

		return rendered

class ProxyMethod(object):
	def __init__(self, iface_name, method):
		self._iface_name = iface_name
		self.__name__ = method.attrib["name"]
		self.__qualname__ = self._iface_name + "." + self.__name__

		inargs  = [(arg.attrib.get("name", ""), arg.attrib["type"]) for arg in method if arg.tag == "arg" and arg.attrib["direction"] == "in"]
		self._outargs = [arg.attrib["type"] for arg in method if arg.tag == "arg" and arg.attrib["direction"] == "out"]
		self._sinargs  = "(" + "".join(x[1] for x in inargs) + ")"
		self._soutargs = "(" + "".join(self._outargs) + ")"

		self_param = Parameter("self", Parameter.POSITIONAL_ONLY)
		pos_params = [Parameter(a[0] if a[0] else "arg" + str(i), Parameter.POSITIONAL_ONLY, annotation=a[1]) for i, a in enumerate(inargs)]
		ret_type = Signature.empty if len(self._outargs) == 0 else self._outargs[0] if len(self._outargs) == 1 else "(" + ", ".join(self._outargs) + ")"

		self.__signature__ = DBUSSignature([self_param] + pos_params, return_annotation=ret_type)

		if put_signature_in_doc:
			self.__doc__ = self.__name__ + str(self.__signature__)

	def __call__(self, instance, *args):
		ret = instance._bus.con.call_sync(
			instance._bus_name, instance._path,
			self._iface_name, self.__name__, GLib.Variant(self._sinargs, args), GLib.VariantType.new(self._soutargs),
			0, instance._bus.timeout, None).unpack()

		if len(self._outargs) == 0:
			return None
		elif len(self._outargs) == 1:
			return ret[0]
		else:
			return ret

	def __get__(self, instance, owner):
		if instance is None:
			return self

		return bound_method(self, instance)

	def __repr__(self):
		return "<function " + self.__qualname__ + " at 0x" + format(id(self), "x") + ">"
