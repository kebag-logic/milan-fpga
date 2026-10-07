#!/bin/bash
# bg.sh NAME CMD... : run CMD detached in the clone, log to receipts/NAME.log, rc to receipts/NAME.rc
. "$(dirname "$0")/env.sh"
name=$1; shift; cd $R
setsid nohup bash -c 'start=$(date +%s); "$@"; rc=$?; echo "rc=$rc elapsed=$(( $(date +%s)-start ))s" > '"$P/receipts/$name.rc" _ "$@" > $P/receipts/$name.log 2>&1 < /dev/null &
echo started $name
