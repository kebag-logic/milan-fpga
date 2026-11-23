#!/usr/bin/env bash
# Run one command detached with its own log and rc file: bg.sh <name> <dir> <cmd...>
name=$1; dir=$2; shift 2
log=$REVIEWS/950-r882-2-packet/receipts/$name.log
rcf=$REVIEWS/950-r882-2-packet/receipts/$name.rc
mkdir -p "$(dirname "$log")"
rm -f "$rcf"
( cd "$dir" && /usr/bin/time -v "$@" ) > "$log" 2>&1 < /dev/null
echo $? > "$rcf"
