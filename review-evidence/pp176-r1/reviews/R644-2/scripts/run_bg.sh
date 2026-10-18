#!/bin/sh
# run_bg.sh NAME DIR CMD... : run CMD in DIR, log to receipts/NAME.log, rc to receipts/NAME.rc
P=$(cd "$(dirname "$0")/.." && pwd); n=$1; d=$2; shift 2
( cd "$d" && "$@" ) > "$P/receipts/$n.log" 2>&1; echo $? > "$P/receipts/$n.rc"
