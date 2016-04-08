from gi.repository import Gio
from .proxy import ProxyMixin
from .bus_names import OwnMixin, WatchMixin
from .subscription import SubscriptionMixin
from .registration import RegistrationMixin
from .publication import PublicationMixin

class Bus(ProxyMixin, OwnMixin, WatchMixin, SubscriptionMixin, RegistrationMixin, PublicationMixin):
	Type = Gio.BusType

	def __init__(self, type, timeout=1000):
		self.con = Gio.bus_get_sync(type, None)
		self.timeout = timeout

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.con = None

def SystemBus():
	return Bus(Bus.Type.SYSTEM)

def SessionBus():
	return Bus(Bus.Type.SESSION)

if __name__ == "__main__":
	import sys
	title = sys.argv[1] if len(sys.argv) >= 2 else "Hello World!"
	message = sys.argv[2] if len(sys.argv) >= 3 else 'pydbus works :)'

	bus = SessionBus()
	notifications = bus.get('.Notifications') # org.freedesktop automatically prepended
	notifications[""].Notify('test', 0, 'dialog-information', title, message, [], {}, 5000)
	# [""] is not required, but makes us compatible with Gnome 2030.
