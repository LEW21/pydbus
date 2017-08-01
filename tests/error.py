from pydbus.error import ErrorRegistration


class ExceptionA(Exception):
	pass


class ExceptionB(Exception):
	pass


class ExceptionC(Exception):
	pass


class ExceptionD(Exception):
	pass


class ExceptionE(Exception):
	pass


def test_error_mapping():
	r = ErrorRegistration()
	r.map_error(ExceptionA, "net.lew21.pydbus.tests.ErrorA")
	r.map_error(ExceptionB, "net.lew21.pydbus.tests.ErrorB")
	r.map_error(ExceptionC, "net.lew21.pydbus.tests.ErrorC")

	assert r.is_registered_exception(ExceptionA("Test"))
	assert r.is_registered_exception(ExceptionB("Test"))
	assert r.is_registered_exception(ExceptionC("Test"))
	assert not r.is_registered_exception(ExceptionD("Test"))
	assert not r.is_registered_exception(ExceptionE("Test"))

	assert r.get_dbus_name(ExceptionA("Test")) == "net.lew21.pydbus.tests.ErrorA"
	assert r.get_dbus_name(ExceptionB("Test")) == "net.lew21.pydbus.tests.ErrorB"
	assert r.get_dbus_name(ExceptionC("Test")) == "net.lew21.pydbus.tests.ErrorC"

	assert r.get_exception_class("net.lew21.pydbus.tests.ErrorA") == ExceptionA
	assert r.get_exception_class("net.lew21.pydbus.tests.ErrorB") == ExceptionB
	assert r.get_exception_class("net.lew21.pydbus.tests.ErrorC") == ExceptionC
	assert r.get_exception_class("net.lew21.pydbus.tests.ErrorD") is None
	assert r.get_exception_class("net.lew21.pydbus.tests.ErrorE") is None

	r.map_by_default(ExceptionD)
	assert not r.is_registered_exception(ExceptionD("Test"))
	assert r.get_exception_class("net.lew21.pydbus.tests.ErrorD") == ExceptionD
	assert r.get_exception_class("net.lew21.pydbus.tests.ErrorE") == ExceptionD


def test_transform_message():
	r = ErrorRegistration()
	n1 = "net.lew21.pydbus.tests.ErrorA"
	m1 = "GDBus.Error:net.lew21.pydbus.tests.ErrorA: Message1"

	n2 = "net.lew21.pydbus.tests.ErrorB"
	m2 = "GDBus.Error:net.lew21.pydbus.tests.ErrorB: Message2"

	assert r.transform_message(n1, m1) == "Message1"
	assert r.transform_message(n2, m2) == "Message2"
	assert r.transform_message(n1, m2) == m2
	assert r.transform_message(n2, m1) == m1


test_error_mapping()
test_transform_message()
