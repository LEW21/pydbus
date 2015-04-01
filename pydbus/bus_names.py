from gi.repository import Gio

class NameOwner(object):
	Flags = Gio.BusNameOwnerFlags
	__slots__ = ("id")

	def __init__(self, con, name, flags, name_aquired_handler, name_lost_handler):
		self.id = Gio.bus_own_name_on_connection(con, name, flags, name_aquired_handler, name_lost_handler)

	def unown(self):
		Gio.bus_unown_name(self.id)
		self.id = None

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if not self.id is None:
			self.unown()

class NameWatcher(object):
	Flags = Gio.BusNameWatcherFlags
	__slots__ = ("id")

	def __init__(self, con, name, flags, name_appeared_handler, name_vanished_handler):
		self.id = Gio.bus_watch_name_on_connection(con, name, flags, name_appeared_handler, name_vanished_handler)

	def unwatch(self):
		Gio.bus_unwatch_name(self.id)
		self.id = None

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if not self.id is None:
			self.unwatch()

class OwnMixin(object):
	__slots__ = ()
	NameOwnerFlags = NameOwner.Flags

	def own_name(self, name, flags=0, name_aquired=None, name_lost=None):
		"""Asynchronously aquires a bus name.

		Starts acquiring name on the bus specified by bus_type and calls
		name_acquired and name_lost when the name is acquired respectively lost.

		To receive name_aquired and name_lost callbacks, you need GLib main loop.
		You can execute it with GObject.MainLoop().run().

		Parameters
		----------
		name : string
			Bus name to aquire
		flags : NameOwnerFlags, optional
		name_aquired : callable, optional
			Invoked when name is acquired
		name_lost : callable, optional
			Invoked when name is lost

		Returns
		-------
		NameOwner
			An object you can use as a context manager to unown the name later.

		See Also
		--------
		See https://developer.gnome.org/gio/2.44/gio-Owning-Bus-Names.html#g-bus-own-name
		for more information.
		"""
		name_aquired_handler = (lambda con, name: name_aquired()) if name_aquired is not None else None
		name_lost_handler    = (lambda con, name: name_lost())    if name_lost    is not None else None
		return NameOwner(self.con, name, flags, name_aquired_handler, name_lost_handler)

	def unown_name(self, name_owner):
		"""Stops owning a name.
		
		Deprecated. Use name_owner.unown() or use name_owner in a with statement.
		
		Parameters
		----------
		name_owner : NameOwner
			Object returned by own_name().
		"""
		name_owner.unown()

class WatchMixin(object):
	__slots__ = ()
	NameWatcherFlags = NameWatcher.Flags

	def watch_name(self, name, flags=0, name_appeared=None, name_vanished=None):
		"""Asynchronously watches a bus name.
		
		Starts watching name on the bus specified by bus_type and calls
		name_appeared and name_vanished when the name is known to have a owner
		respectively known to lose its owner.

		To receive name_appeared and name_vanished callbacks, you need GLib main loop.
		You can execute it with GObject.MainLoop().run().

		Parameters
		----------
		name : string
			Bus name to watch
		flags : NameWatcherFlags, optional
		name_appeared : callable, optional
			Invoked when name is known to exist
			Called as name_appeared(name_owner).
		name_vanished : callable, optional
			Invoked when name is known to not exist

		Returns
		-------
		NameWatcher
			An object you can use as a context manager to unwatch the name later.

		See Also
		--------
		See https://developer.gnome.org/gio/2.44/gio-Watching-Bus-Names.html#g-bus-watch-name
		for more information.
		"""
		name_appeared_handler = (lambda con, name, name_owner: name_appeared(name_owner)) if name_appeared is not None else None
		name_vanished_handler = (lambda con, name:             name_vanished())           if name_vanished is not None else None
		return NameWatcher(self.con, name, flags, name_appeared_handler, name_vanished_handler)

	def unwatch_name(self, name_watcher):
		"""Stops watching a name.
		
		Deprecated. Use name_watcher.unwatch() or use name_watcher in a with statement.
		
		Parameters
		----------
		name_watcher : NameWatcher
			Object returned by watch_name().
		"""
		name_watcher.unwatch()

if __name__ == "__main__":
	from . import SessionBus
	from gi.repository import GObject

	def echo(x):
		print(x)

	bus = SessionBus()
	bus.watch_name("com.example", 0, echo)
	bus.own_name("com.example")
	GObject.MainLoop().run()
