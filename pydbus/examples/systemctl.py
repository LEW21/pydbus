from pydbus import SystemBus
from gi.repository import Gio

bus = SystemBus()

systemd = bus.get(".systemd1")
#systemd = bus.get("org.freedesktop.systemd1")

manager = systemd[".Manager"]
#manager = systemd["org.freedesktop.systemd1.Manager"]
#manager = systemd # works but may break if systemd adds another interface

import sys

try:
	if len(sys.argv) < 2:
		for unit in manager.ListUnits()[0]:
			print(unit)
	else:
		if sys.argv[1] == "--help":
			help(manager)
		else:
			command = sys.argv[1]
			command = "".join(x.capitalize() for x in command.split("-"))
			result = getattr(manager, command)(*sys.argv[2:])

			for var in result:
				if type(var) == list:
					for line in var:
						print(line)
				else:
					print(var)
except Exception as e:
	print(e)

"""
Examples:

python -m pydbus.examples.systemctl
sudo python -m pydbus.examples.systemctl start-unit cups.service replace
"""
