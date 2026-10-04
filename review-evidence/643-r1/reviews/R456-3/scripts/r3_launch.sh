#!/bin/bash
# R456-3: start one lane detached, with its own log and rc file.
# Usage: r3_launch.sh PACKET NAME COMMAND...   (environment passes through)
P=$1; N=$2; shift 2
mkdir -p "$P/receipts/lanes"
export VALIDATION_TOOLS=${VALIDATION_TOOLS:-$VALIDATION_TOOLS}
setsid nohup bash -c '"$@"; echo "rc=$?" > "'"$P/receipts/lanes/$N.rc"'"' _ "$@" \
  > "$P/receipts/lanes/$N.log" 2>&1 < /dev/null &
echo "launched $N pid $!"
