from gi.repository import GLib
from functools import wraps

def upcast(v):
	v.__class__ = Variant
	return v

def auto_upcast(func):
	@wraps(func)
	def wrapper(*args):
		v = func(*args)
		return upcast(v) if v is not None else None
	return wrapper

def variant_get_bytes(v):
	return v.get_data_as_bytes().get_data()

def variant_children(v):
	return (v.get_child_value(i) for i in range(v.n_children()))

class Variant(GLib.Variant):
	get_variant = auto_upcast(GLib.Variant.get_variant)
	get_maybe = auto_upcast(GLib.Variant.get_maybe)
	get_child_value = auto_upcast(GLib.Variant.get_child_value)
	lookup_value = auto_upcast(GLib.Variant.lookup_value)

	def get_bytes(self):
		return variant_get_bytes(self)

	def unpack(self):
		"""Decompose a GVariant into a native Python object."""

		typestring = self.get_type_string()

		LEAF_ACCESSORS = {
			'b': self.get_boolean,
			'y': self.get_byte,
			'n': self.get_int16,
			'q': self.get_uint16,
			'i': self.get_int32,
			'u': self.get_uint32,
			'x': self.get_int64,
			't': self.get_uint64,
			'h': self.get_handle,
			'd': self.get_double,
			's': self.get_string,
			'o': self.get_string,  # object path
			'g': self.get_string,  # signature
			'ay': self.get_bytes,
		}

		# simple values
		la = LEAF_ACCESSORS.get(typestring)
		if la:
			return la()

		# tuple
		if typestring.startswith('('):
			return tuple(c.unpack() for c in variant_children(self))

		# dictionary
		if typestring.startswith('a{'):
			return {v.get_child_value(0).unpack(): v.get_child_value(1).unpack() for v in variant_children(self)}

		# array
		if typestring.startswith('a'):
			return list(c.unpack() for c in variant_children(self))

		# variant (PASS THRU, don't unbox anything transparently, as we don't auto-box)
		if typestring.startswith('v'):
			return self.get_variant()

		# maybe
		if typestring.startswith('m'):
			m = self.get_maybe()
			return m.unpack() if m else None

		raise NotImplementedError('unsupported GVariant type ' + typestring)
