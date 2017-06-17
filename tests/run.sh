#!/bin/sh
set -e
set -x
TESTS_DIR=$(dirname "$0")
SRC_DIR=`/bin/readlink -f "$TESTS_DIR/.."`
#eval `dbus-launch --sh-syntax`
export $(dbus-launch)
trap 'kill -TERM $DBUS_SESSION_BUS_PID' EXIT

PYTHON=${1:-python}

"$PYTHON" $TESTS_DIR/context.py
"$PYTHON" $TESTS_DIR/identifier.py
#if [ "$2" != "dontpublish" ]
#then
	"$PYTHON" $TESTS_DIR/publish.py
	"$PYTHON" $TESTS_DIR/publish_properties.py
	"$PYTHON" $TESTS_DIR/publish_multiface.py
#fi
echo running unit tests
cd $SRC_DIR/pydbus
"$PYTHON"  $SRC_DIR/pydbus/_unittest.py

