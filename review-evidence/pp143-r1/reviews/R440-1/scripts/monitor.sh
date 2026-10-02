#!/bin/bash
# Samples the unit's memory, OOM events, and the private copies under TMPDIR every 10 s.
. $REVIEWS/pp143-r440-1-packet/scripts/env.sh
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
while [ ! -e $P/scratch/monitor.stop ]; do
  printf '%s mem=%s peak=%s oom_kill=%s copies=%s free_data=%s\n' "$(date -u +%T)" \
    "$(cat $cg/memory.current)" "$(cat $cg/memory.peak 2>/dev/null)" \
    "$(awk '/oom_kill /{print $2}' $cg/memory.events)" \
    "$(ls $TMPDIR | sed 's/-[^-]*$//' | sort | uniq -c | tr -s ' ' | tr '\n' ';')" \
    "$(df --output=avail -h /data | tail -1)"
  ls $TMPDIR >> $P/receipts/monitor_copies.txt
  sleep 10
done
