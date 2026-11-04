#!/usr/bin/env bash
# memgov.sh <runs>: every 2 s read this unit's memory.current; above 9.3 GB stop the process groups listed in
# <runs>/memgov.pgids (campaigns: cycle-bounded simulations, no wall clock), resume them below 7.0 GB; also
# log a sample every 10 s. Stops when <runs>/memgov.stop exists, resuming first.
R=$1
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
L=$R/memgov.log
stopped=0; n=0
while [ ! -f $R/memgov.stop ]; do
  cur=$(cat $CG/memory.current)
  pg=$(cat $R/memgov.pgids 2>/dev/null)
  if [ $stopped = 0 ] && [ "$cur" -gt 9300000000 ]; then
    for g in $pg; do kill -STOP -- -$g 2>/dev/null; done; stopped=1; echo "$(date +%s) $cur stop $pg" >> $L
  elif [ $stopped = 1 ] && [ "$cur" -lt 7000000000 ]; then
    for g in $pg; do kill -CONT -- -$g 2>/dev/null; done; stopped=0; echo "$(date +%s) $cur resume" >> $L
  fi
  n=$((n+1)); [ $((n % 5)) = 0 ] && echo "$(date +%s) $cur" >> $R/memory-samples.log
  sleep 2
done
for g in $(cat $R/memgov.pgids 2>/dev/null); do kill -CONT -- -$g 2>/dev/null; done
echo "$(date +%s) end" >> $L
