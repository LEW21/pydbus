from gi.repository import Gio

# signature type code
TYPE_FD = "h"

def is_supported(conn):
	"""
	Check if the message bus supports passing of Unix file descriptors.
	"""
	return conn.get_capabilities() & Gio.DBusCapabilityFlags.UNIX_FD_PASSING


def extract(params, signature, fd_list):
	"""
	Extract any file descriptors from a UnixFDList (e.g. after
	receiving from D-Bus) to a parameter list.
	Receiver must call os.dup on any fd it decides to keep/use.
	"""
	if not fd_list:
		return params
	return [fd_list.get(0)
		if arg == TYPE_FD
		else val
		for val, arg
		in zip(params, signature)]


def make_fd_list(params, signature, steal=False):
	"""
	Embed any unix file descriptors in a parameter list into a
	UnixFDList (for D-Bus-dispatch).
	If steal is true, the responsibility for closing the file
	descriptors are transferred to the UnixFDList object.
	If steal is false, the file descriptors will be duplicated
	and the caller must close the original file descriptors.
	"""
	if not any(arg
		   for arg in signature
		   if arg == TYPE_FD):
		return None

	fds = [param
	       for param, arg
	       in zip(params, signature)
	       if arg == TYPE_FD]

	if steal:
		return Gio.UnixFDList.new_from_array(fds)

	fd_list = Gio.UnixFDList()
	for fd in fds:
		fd_list.append(fd)
	return fd_list
