from gi.repository import Gio
from .proxy import ProxyMixin
from .request_name import RequestNameMixin
from .bus_names import OwnMixin, WatchMixin
from .subscription import SubscriptionMixin
from .registration import RegistrationMixin
from .publication import PublicationMixin

class Bus(ProxyMixin, RequestNameMixin, OwnMixin, WatchMixin, SubscriptionMixin, RegistrationMixin, PublicationMixin):
	Type = Gio.BusType

	def __init__(self, type, timeout=1000):
		self.con = Gio.bus_get_sync(type, None)
		self.timeout = timeout

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.con = None

	@property
	def dbus(self):
		try:
			return self._dbus
		except AttributeError:
			self._dbus = self.get(".DBus")[""]
			return self._dbus

	@property
	def polkit_authority(self):
		try:
			return self._polkit_authority
		except AttributeError:
			self._polkit_authority = self.get(".PolicyKit1", "Authority")
			return self._polkit_authority

def SystemBus(timeout=1000):
	return Bus(Bus.Type.SYSTEM, timeout=timeout)

def SessionBus(timeout=1000):
	return Bus(Bus.Type.SESSION, timeout=timeout)

if __name__ == "__main__":
	import sys
	title = sys.argv[1] if len(sys.argv) >= 2 else "Hello World!"
	message = sys.argv[2] if len(sys.argv) >= 3 else 'pydbus works :)'

	bus = SessionBus()
	notifications = bus.get('.Notifications') # org.freedesktop automatically prepended
	notifications[""].Notify('test', 0, 'dialog-information', title, message, [], {}, 5000)
	# [""] is not required, but makes us compatible with Gnome 2030.
