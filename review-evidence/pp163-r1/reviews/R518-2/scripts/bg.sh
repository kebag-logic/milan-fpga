#!/bin/sh
# Start one command detached, with its own log and rc file, and print its pid.
# usage: bg.sh NAME DIR CMD...   -> $LOGDIR/NAME.log, $LOGDIR/NAME.rc, $LOGDIR/NAME.time
# LOGDIR defaults to the packet's receipts/runs. The rc file appears only when done.
set -eu
name=$1; dir=$2; shift 2
logdir=${LOGDIR:-$(cd "$(dirname "$0")/.." && pwd)/receipts/runs}
mkdir -p "$logdir"
rm -f "$logdir/$name.rc"
(
  cd "$dir"
  start=$(date +%s)
  set +e
  /usr/bin/time -v -o "$logdir/$name.time" "$@" > "$logdir/$name.log" 2>&1
  rc=$?
  echo "elapsed_s $(( $(date +%s) - start ))" >> "$logdir/$name.time"
  echo "$rc" > "$logdir/$name.rc"
) < /dev/null > /dev/null 2>&1 &
echo "$name started pid $!"
