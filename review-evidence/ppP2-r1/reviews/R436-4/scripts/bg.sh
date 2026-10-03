#!/usr/bin/env bash
# bg.sh NAME DIR CMD... : run CMD in DIR detached, log to receipts/NAME.log, rc to receipts/NAME.rc
P=$(cd "$(dirname "$0")/.." && pwd)
name=$1; dir=$2; shift 2
export VERILATOR=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
rm -f "$P/receipts/$name.rc"
( cd "$dir" && nohup bash -c "$*" > "$P/receipts/$name.log" 2>&1; echo $? > "$P/receipts/$name.rc" ) >/dev/null 2>&1 &
