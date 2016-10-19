#!/bin/sh
set -e

cd "$(dirname "$(dirname "$0")")"

ADDRESS_FILE=$(mktemp /tmp/pydbustest.XXXXXXXXX)
PID_FILE=$(mktemp /tmp/pydbustest.XXXXXXXXX)

dbus-daemon --session --print-address=0 --print-pid=1 --fork 0>"$ADDRESS_FILE" 1>"$PID_FILE"

export DBUS_SESSION_BUS_ADDRESS=$(cat "$ADDRESS_FILE")
PID=$(cat "$PID_FILE")

trap 'kill -TERM $PID' EXIT

rm "$ADDRESS_FILE" "$PID_FILE"

PYTHON=${1:-python}

"$PYTHON" -m pytest -v pydbus/tests/identifier.py pydbus/tests/context.py
if [ "$2" != "dontpublish" ]
then
	"$PYTHON" -m pydbus.tests.publish
	"$PYTHON" -m pydbus.tests.publish_properties
	"$PYTHON" -m pydbus.tests.publish_multiface
fi
