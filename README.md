pydbus
======

Pythonic DBus library.

It's based on PyGI, the Python GObject Introspection bindings, which is the recommended way to use GLib from Python.

It's pythonic!

```python
from pydbus import SessionBus

bus = SessionBus()
notifications = bus.get('.Notifications')

notifications.Notify('test', 0, 'dialog-information', "Hello World!", "pydbus works :)", [], {}, 5000)
```

```python
from pydbus import SystemBus

bus = SystemBus()
systemd = bus.get(".systemd1")

for unit in systemd.ListUnits()[0]:
    print(unit)
```
