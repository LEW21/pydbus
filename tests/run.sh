#!/bin/sh
set -e

eval `dbus-launch --sh-syntax`

trap 'kill -TERM $DBUS_SESSION_BUS_PID' EXIT

PYTHON=${1:-python}

"$PYTHON" -m pydbus.tests.context
"$PYTHON" -m pydbus.tests.identifier
if [ "$2" != "dontpublish" ]
then
	"$PYTHON" -m pydbus.tests.publish
	"$PYTHON" -m pydbus.tests.publish_properties
	"$PYTHON" -m pydbus.tests.publish_multiface
fi
