#!/usr/bin/env bash
# memgov.sh <runs> <pgid>...: every 2 s read this unit's memory.current; above 9.0 GB stop the given process groups
# (campaigns: their simulations are cycle-bounded and their drivers keep no wall clock), resume them below 7.0 GB.
# Logs each stop and resume. Stops when <runs>/memgov.stop exists, resuming first.
R=$1; shift
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
L=$R/memgov.log
stopped=0
while [ ! -f $R/memgov.stop ]; do
  cur=$(cat $CG/memory.current)
  if [ $stopped = 0 ] && [ "$cur" -gt 9000000000 ]; then
    for g in "$@"; do kill -STOP -- -$g 2>/dev/null; done; stopped=1; echo "$(date +%s) $cur stop $*" >> $L
  elif [ $stopped = 1 ] && [ "$cur" -lt 7000000000 ]; then
    for g in "$@"; do kill -CONT -- -$g 2>/dev/null; done; stopped=0; echo "$(date +%s) $cur resume" >> $L
  fi
  sleep 2
done
for g in "$@"; do kill -CONT -- -$g 2>/dev/null; done
echo "$(date +%s) end" >> $L
