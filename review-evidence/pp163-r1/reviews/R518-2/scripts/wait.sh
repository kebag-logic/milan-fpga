#!/bin/sh
# Wait (foreground, at most MAXS seconds, default 540) until every named job has its rc file.
# usage: wait.sh NAME...   prints each job's rc, or PENDING, and the unit's memory peak so far.
logdir=${LOGDIR:-$(cd "$(dirname "$0")/.." && pwd)/receipts/runs}
maxs=${MAXS:-540}
t=0
while :; do
  pending=0
  for n in "$@"; do [ -f "$logdir/$n.rc" ] || pending=1; done
  [ $pending = 0 ] && break
  [ $t -ge "$maxs" ] && break
  sleep 10; t=$((t + 10))
done
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
echo "unit memory.current $(cat "$cg/memory.current") peak $(cat "$cg/memory.peak" 2>/dev/null)"
for n in "$@"; do
  if [ -f "$logdir/$n.rc" ]; then echo "$n rc=$(cat "$logdir/$n.rc") $(grep elapsed_s "$logdir/$n.time")"; else echo "$n PENDING"; fi
done
