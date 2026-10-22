#!/bin/bash
# memhigh.sh <file>: append a sample, with the top resident processes, whenever anon exceeds 5 GB.
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup | head -1)
while true; do
  anon=$(awk '$1=="anon"{print $2}' $cg/memory.stat)
  if [ "$anon" -gt 5000000000 ]; then
    { echo "$(date -Is) anon=$anon current=$(cat $cg/memory.current)"; ps -eo rss,args --sort=-rss | head -4 | cut -c1-160; } >> "$1"
  fi
  sleep 5
done
