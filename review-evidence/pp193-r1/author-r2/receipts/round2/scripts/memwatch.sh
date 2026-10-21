#!/usr/bin/env bash
# keep the unit's MemoryCurrent under 9 GB: reclaim page cache above 8 GB;
# log current/anon/shmem every minute
C=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/milan-pp193-a661d.service
log=<scratch>/r2/rec/memwatch.log
i=0
while :; do
  cur=$(cat $C/memory.current)
  if [ "$cur" -gt 8589934592 ]; then echo 2G > $C/memory.reclaim 2>/dev/null; fi
  if [ $((i % 6)) -eq 0 ]; then
    an=$(awk '$1=="anon"{print $2}' $C/memory.stat); sh=$(awk '$1=="shmem"{print $2}' $C/memory.stat)
    echo "$(date +%H:%M:%S) cur=$((cur>>20))M anon=$((an>>20))M shmem=$((sh>>20))M" >> $log
  fi
  i=$((i+1)); sleep 10
done
