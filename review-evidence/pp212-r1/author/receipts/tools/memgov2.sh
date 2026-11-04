#!/usr/bin/env bash
# memgov2.sh <runs>: every 2 s read this unit's anonymous + shmem memory (memory.stat); above 8.5 GB stop the
# process groups listed in <runs>/memgov.pgids (campaigns: cycle-bounded simulations, no wall clock), resume them
# below 6.5 GB. memory.current, which also counts reclaimable page cache, is logged beside it every 10 s,
# and above 9.0 GB the governor asks the kernel to reclaim 1.5 GB of it (memory.reclaim), so it stays under 10 GB.
# Stops when <runs>/memgov.stop exists, resuming first.
R=$1
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
L=$R/memgov.log
stopped=0; n=0
while [ ! -f $R/memgov.stop ]; do
  used=$(awk '$1=="anon"||$1=="shmem"{s+=$2} END{print s}' $CG/memory.stat)
  pg=$(cat $R/memgov.pgids 2>/dev/null)
  if [ $stopped = 0 ] && [ "$used" -gt 8500000000 ]; then
    for g in $pg; do kill -STOP -- -$g 2>/dev/null; done; stopped=1; echo "$(date +%s) anon $used stop $pg" >> $L
  elif [ $stopped = 1 ] && [ "$used" -lt 6500000000 ]; then
    for g in $pg; do kill -CONT -- -$g 2>/dev/null; done; stopped=0; echo "$(date +%s) anon $used resume" >> $L
  fi
  cur=$(cat $CG/memory.current)
  if [ "$cur" -gt 9000000000 ]; then echo 1500M > $CG/memory.reclaim 2>/dev/null; echo "$(date +%s) current $cur reclaim" >> $L; fi
  n=$((n+1)); [ $((n % 5)) = 0 ] && echo "$(date +%s) current $(cat $CG/memory.current) anon $used" >> $R/memory-samples.log
  sleep 2
done
for g in $(cat $R/memgov.pgids 2>/dev/null); do kill -CONT -- -$g 2>/dev/null; done
echo "$(date +%s) end" >> $L
