#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Anselm Kruis
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#

"""
A decorator for Polkit authorization
"""

from __future__ import print_function, absolute_import

from gi.repository import GLib, Polkit, Gio
import functools
from pydbus import registration, generic
# import traceback

__all__ = ['PolkitAuthorization']


class PolkitAuthorization(object):
	@staticmethod
	def NotAuthorizedError(message="Not authorized to perform operation"):
		return GLib.Error.new_literal(Polkit.error_quark(), message, Polkit.Error.NOT_AUTHORIZED)

	def __init__(self, action_id, details=None, flags=Polkit.CheckAuthorizationFlags.ALLOW_USER_INTERACTION):
		if callable(action_id):
			raise TypeError("PolkitAuthorization needs an action id")
		self.action_id = action_id
		self.details = details
		self.flags = flags

	def __call__(self, func):
		func_info = generic.inspect_function(func, flag_names=('async',), arg_names=('dbus_bus', 'dbus_method_invocation', "polkit_is_authorized"))
		is_async = func_info['async']
		needs_dbus_method_invocation = func_info["dbus_method_invocation"]
		needs_dbus_bus = func_info["dbus_bus"]
		needs_polkit_is_authorized = func_info["polkit_is_authorized"]

		@functools.wraps(func)
		def wrapper(*args, **kw):
			bus = kw['dbus_bus'] if needs_dbus_bus else kw.pop('dbus_bus')
			method_invocation = kw['dbus_method_invocation'] if needs_dbus_method_invocation else kw.pop('dbus_method_invocation')
			try:
				cancellable = Gio.Cancellable()
				state = dict(bus=bus,
							method_invocation=method_invocation,
							func=func,
							is_async=is_async,
							needs_polkit_is_authorized=needs_polkit_is_authorized,
							cancellable=cancellable,
							args=args,
							kw=kw)
				timeout = bus.timeout
				if timeout == -1:
					# -1 indicates a default value
					timeout = 25000  # DBus default

				GLib.timeout_add(timeout, cancellable.cancel)
				Polkit.Authority.get_async(cancellable, self._cb_get_authority_ready, state)
			except Exception as e:
				# traceback.print_exc()  # FIXME: better error reporting. logging?
				method_invocation.return_exception(e)

		wrapper.async = True
		wrapper.arg_dbus_bus = True
		wrapper.arg_dbus_method_invocation = True
		return wrapper

	def _cb_get_authority_ready(self, source_object, res, state):
		# source_object is None
		method_invocation = state['method_invocation']
		try:
			authority = Polkit.Authority.get_finish(res)
			assert authority is not None

			sender = method_invocation.get_sender()
			dbus_service = state['bus'].get('.DBus')['']
			sender_pid = dbus_service.GetConnectionUnixProcessID(sender)  # synchronous call for now
			subject = Polkit.UnixProcess.new(sender_pid)

			authority.check_authorization(subject,
										self.action_id,
										self.details,
										self.flags,
										state['cancellable'],
										self._cb_check_authorization_ready,
										state)
		except Exception as e:
			# traceback.print_exc()  # FIXME: better error reporting. logging?
			method_invocation.return_exception(e)

	def _cb_check_authorization_ready(self, authority, res, state):
		method_invocation = state['method_invocation']
		needs_polkit_is_authorized = state['needs_polkit_is_authorized']
		try:
			result = authority.check_authorization_finish(res)
			is_authorized = result.get_is_authorized()
			if not needs_polkit_is_authorized and not is_authorized:
				method_invocation.return_exception(self.NotAuthorizedError())
				return

			if needs_polkit_is_authorized:
				state['kw']['polkit_is_authorized'] = is_authorized

			result = state['func'](*state['args'], **state['kw'])
			if not (state['is_async'] or result is registration.METHOD_IS_ASYNC):
				method_invocation.return_value(result)

		except Exception as e:
			# traceback.print_exc()  # FIXME: better error reporting. logging?
			method_invocation.return_exception(e)
