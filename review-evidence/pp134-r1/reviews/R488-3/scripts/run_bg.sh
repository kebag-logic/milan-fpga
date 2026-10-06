#!/bin/bash
# run_bg.sh NAME CMD... : run CMD detached with receipts/NAME.log and receipts/NAME.rc
P=${P:-$REVIEWS/pp134-r488-3-packet}
. "$P/scripts/env.sh"
name=$1; shift
rm -f "$P/receipts/$name.rc"
( start=$(date +%s); "$@" > "$P/receipts/$name.log" 2>&1; rc=$?; echo "$rc $(( $(date +%s) - start ))s" > "$P/receipts/$name.rc" ) </dev/null >/dev/null 2>&1 &
echo "started $name pid $!"
