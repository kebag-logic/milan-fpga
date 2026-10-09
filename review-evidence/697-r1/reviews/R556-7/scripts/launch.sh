#!/bin/sh
# launch.sh NAME DIR CMD... : run CMD in DIR detached, log to receipts/NAME.log, rc to receipts/NAME.rc
name=$1; dir=$2; shift 2
: "${PACKET:?set PACKET}"
rm -f "$PACKET/receipts/$name.rc"
( cd "$dir" && /usr/bin/time -v "$@" > "$PACKET/receipts/$name.log" 2>&1; echo $? > "$PACKET/receipts/$name.rc" ) </dev/null >/dev/null 2>&1 &
echo "launched $name"
