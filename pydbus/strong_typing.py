"""Decorators for methods and properties to strongly typed the values."""
import inspect

from pydbus.xml_generator import get_arguments


def typed_property(value_type):
	"""
	Decorate a function as a dbus property getter.

	It alreay makes the method a property so another `@property` decorator may
	not be used.
	"""
	def decorate(func):
		func.prop_type = value_type
		return property(func)
	return decorate


def typed_method(argument_types, return_type):
	"""
	Decorate a function as a dbus method.

	Parameters
	----------
	argument_types : tuple
		Required argument types for each argument except the first
	return_type : string
		Type of the returned value, must be None if it returns nothing
	"""
	def decorate(func):
		func.arg_types = argument_types
		func.ret_type = return_type
		get_arguments(func)
		return func
	return decorate
