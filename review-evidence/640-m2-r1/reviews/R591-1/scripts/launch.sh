#!/bin/bash
# launch.sh NAME DIR CMD... : run CMD in DIR detached, log to receipts/NAME.log, rc to receipts/NAME.rc
P="${PACKET:?set PACKET to the packet directory}"
name=$1; dir=$2; shift 2
rm -f "$P/receipts/$name.rc"
( cd "$dir" && env TMPDIR=$P/scratch/tmp PYTHONDONTWRITEBYTECODE=1 "$@" > "$P/receipts/$name.log" 2>&1; echo $? > "$P/receipts/$name.rc" ) </dev/null >/dev/null 2>&1 &
disown
