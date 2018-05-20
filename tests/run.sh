#!/bin/sh
set -e

TESTS_DIR=$(dirname "$0")
eval `dbus-launch --sh-syntax`

trap 'kill -TERM $DBUS_SESSION_BUS_PID' EXIT

PYTHON=${1:-python}

"$PYTHON" $TESTS_DIR/context.py
"$PYTHON" $TESTS_DIR/identifier.py
if [ "$2" != "dontpublish" ]
then
	"$PYTHON" $TESTS_DIR/publish.py
	"$PYTHON" $TESTS_DIR/publish_properties.py
	"$PYTHON" $TESTS_DIR/publish_multiface.py
	"$PYTHON" $TESTS_DIR/dbus_exception.py
fi
