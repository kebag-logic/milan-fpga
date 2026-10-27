#!/bin/sh
# run_bg.sh NAME DIR CMD... : run CMD in DIR detached, logging to
# $PACKET/receipts/NAME.log and writing the exit code to NAME.rc
# PACKET defaults to the directory above this script.
set -u
PACKET=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
name=$1; dir=$2; shift 2
log=$PACKET/receipts/$name.log; rc=$PACKET/receipts/$name.rc
rm -f "$rc"
(
  cd "$dir" || { echo 99 > "$rc"; exit; }
  date -u +%FT%TZ > "$PACKET/receipts/$name.start"
  "$@" > "$log" 2>&1
  echo $? > "$rc.tmp"; mv "$rc.tmp" "$rc"
  date -u +%FT%TZ > "$PACKET/receipts/$name.end"
) </dev/null >/dev/null 2>&1 &
echo "started $name"
