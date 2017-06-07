#!/bin/sh
set -e
set -x
TESTS_DIR=$(dirname "$0")
SRC_DIR=`/bin/readlink -f "$TESTS_DIR/../pydbus"`
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
fi
echo running unit tests
"$PYTHON"  -m $SRC_DIR/_unittest.py
