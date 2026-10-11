#!/bin/sh
# run_bg.sh NAME DIR CMD... : run CMD in DIR detached, log to receipts/NAME.log, rc to receipts/NAME.rc
P=$(cd "$(dirname "$0")/.." && pwd)
name=$1; dir=$2; shift 2
rm -f "$P/receipts/$name.rc"
( cd "$dir" && { date -u +%FT%TZ; echo "+ $*"; } > "$P/receipts/$name.log" && \
  "$@" >> "$P/receipts/$name.log" 2>&1; echo $? > "$P/receipts/$name.rc"; date -u +%FT%TZ >> "$P/receipts/$name.log" ) </dev/null >/dev/null 2>&1 &
