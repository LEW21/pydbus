#!/bin/sh
set -e

ADDRESS_FILE=$(mktemp /tmp/pydbustest.XXXXXXXXX)
PID_FILE=$(mktemp /tmp/pydbustest.XXXXXXXXX)

dbus-daemon --session --print-address=0 --print-pid=1 --fork 0>"$ADDRESS_FILE" 1>"$PID_FILE"

export DBUS_SESSION_BUS_ADDRESS=$(cat "$ADDRESS_FILE")
PID=$(cat "$PID_FILE")

trap 'kill -TERM $PID' EXIT

rm "$ADDRESS_FILE" "$PID_FILE"

PYTHON=${1:-python}

"$PYTHON" -m pydbus.examples.notifications_server &
NOTIF_PID=$!
trap 'kill -TERM $PID $NOTIF_PID' EXIT

sleep 1

"$PYTHON" -m pydbus.tests.context
"$PYTHON" -m pydbus.tests.green
"$PYTHON" -m pydbus.tests.identifier
"$PYTHON" -m pydbus.tests.publish
"$PYTHON" -m pydbus.tests.publish_concurrent
"$PYTHON" -m pydbus.tests.publish_multiface
