#!/bin/sh
# Start one named job in the background with its own log and rc file.
# Usage: launch.sh <receipts dir> <name> <workdir> <command...>
R=$1; N=$2; D=$3; shift 3
rm -f "$R/$N.rc"
( cd "$D" && "$@" > "$R/$N.log" 2>&1; echo $? > "$R/$N.rc" ) &
