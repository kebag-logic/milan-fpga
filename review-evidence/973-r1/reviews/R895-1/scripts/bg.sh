#!/bin/bash
# bg.sh NAME CMD...: run CMD detached with its log at $P/receipts/NAME.log and its exit status at $P/receipts/NAME.rc
n=$1; shift
rm -f "$P/receipts/$n.rc"
( "$@" > "$P/receipts/$n.log" 2>&1; echo $? > "$P/receipts/$n.rc" ) </dev/null &
