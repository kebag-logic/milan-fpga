#!/bin/bash
# usage: monitor.sh PHASE NAME...   (runs until every NAME has an rc file)
# Every 5 s: the unit cgroup's memory.current and memory.peak, and for each
# campaign the live unit copies under scratch/tmp-NAME (name, obj dirs, *.hex).
set -u
P=${PACKET:-$REVIEWS/pp143-r441-1-packet}
C=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
phase=$1; shift
log=$P/receipts/monitor-$phase.log; seen=$P/receipts/monitor-$phase.dirs
: > "$log"; : > "$seen.raw"
while :; do
  done_all=1
  for n in "$@"; do [ -f "$P/receipts/$n/rc" ] || done_all=0; done
  ts=$(date +%s)
  echo "$ts mem.current=$(cat $C/memory.current) anon=$(awk '/^anon /{print $2}' $C/memory.stat) mem.peak=$(cat $C/memory.peak)" >> "$log"
  for n in "$@"; do
    d=$P/scratch/tmp-$n
    live=$(find "$d" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
    echo "$ts $n live_copies=$live" >> "$log"
    find "$d" -mindepth 1 -maxdepth 1 -type d -printf "$n %f\n" 2>/dev/null >> "$seen.raw"
    find "$d" -mindepth 2 -maxdepth 4 \( -name 'obj*' -type d -o -name '*.hex' \) -printf "$ts $n %P\n" 2>/dev/null >> "$log"
  done
  [ $done_all = 1 ] && break
  sleep 5
done
sort -u "$seen.raw" > "$seen"; rm -f "$seen.raw"
