#!/bin/bash
# bg.sh NAME DIR CMD... : run CMD in DIR detached, log to receipts/runs/NAME.log, rc to NAME.rc
. $REVIEWS/665f3-r530-5-packet/scripts/env.sh
N=$1; D=$2; shift 2; R=$P/receipts/runs
rm -f $R/$N.rc
cd "$D" && setsid nohup bash -c '"$@" > "$0.log" 2>&1; echo $? > "$0.rc"' "$R/$N" "$@" < /dev/null > /dev/null 2>&1 &
