#!/bin/bash
# memwatch.sh <file>: sample this lane service's memory.current and anon every 10 s; keep the peaks.
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup | head -1)
peak=0; peak_anon=0
while true; do
  cur=$(cat $cg/memory.current); anon=$(awk '$1=="anon"{print $2}' $cg/memory.stat)
  [ "$cur" -gt "$peak" ] && peak=$cur; [ "$anon" -gt "$peak_anon" ] && peak_anon=$anon
  echo "$(date -Is) current=$cur anon=$anon peak=$peak peak_anon=$peak_anon cg=$cg" > "$1"
  sleep 10
done
