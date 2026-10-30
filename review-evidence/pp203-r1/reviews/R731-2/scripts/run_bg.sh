#!/bin/sh
# run_bg.sh NAME DIR CMD... : run CMD in DIR detached, log to receipts/NAME.log, rc to receipts/NAME.rc
P=$(cd "$(dirname "$0")/.." && pwd)
name=$1; dir=$2; shift 2
rm -f "$P/receipts/$name.rc"
( cd "$dir" && /usr/bin/time -v "$@" > "$P/receipts/$name.log" 2>&1; echo $? > "$P/receipts/$name.rc" ) </dev/null >/dev/null 2>&1 &
echo "started $name pid $!"
