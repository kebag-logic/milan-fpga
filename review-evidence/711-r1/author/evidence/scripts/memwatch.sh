#!/bin/bash
# Reclaim page cache when this service's MemoryCurrent passes 7.5 GiB; log current and anon each minute.
cg=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/milan-711-a589.service
n=0
while :; do
  cur=$(cat $cg/memory.current)
  if [ "$cur" -gt 8053063680 ]; then echo 1G > $cg/memory.reclaim 2>/dev/null; echo "$(date -Is) reclaimed at $cur"; fi
  n=$((n+1))
  if [ $((n % 6)) -eq 0 ]; then echo "$(date -Is) current $cur anon $(awk '/^anon /{print $2}' $cg/memory.stat)"; fi
  sleep 10
done
