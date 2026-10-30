#!/usr/bin/env bash
# every 10 s: log this unit's memory (current, anon, file); above 7.5 GB, ask the cgroup to reclaim page cache.
# Stops when $1/memguard.stop exists.
R=$1
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
L=$R/memguard.log
while [ ! -f $R/memguard.stop ]; do
  cur=$(cat $CG/memory.current)
  anon=$(awk '$1=="anon"{print $2}' $CG/memory.stat)
  file=$(awk '$1=="file"{print $2}' $CG/memory.stat)
  act=""
  if [ "$cur" -gt 7500000000 ]; then echo 2G > $CG/memory.reclaim 2>/dev/null; act=reclaim; fi
  echo "$(date +%s) $cur $anon $file $act" >> $L
  sleep 10
done
