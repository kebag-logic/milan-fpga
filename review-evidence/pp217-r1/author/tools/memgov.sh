#!/usr/bin/env bash
# memgov.sh: every 2 s, ask the kernel to reclaim page cache from this unit when memory.current is above 8.0 GB
# (memory.reclaim; no process is stopped); logs each reclaim. While anon is above 6.5 GB the campaign Verilator
# builds are capped at -j1 (vl-cap/build-j), back to 2 below 5 GB.
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
CAP=$(cd "$(dirname "$0")" && pwd)/vl-cap/build-j
while :; do
  cur=$(cat $CG/memory.current)
  anon=$(grep '^anon ' $CG/memory.stat | cut -d' ' -f2)
  if [ "$anon" -gt 6500000000 ] && [ "$(cat $CAP)" != 1 ]; then echo 1 > $CAP; echo "$(date +%T) anon=$((anon/1000000))MB build-j 1"; fi
  if [ "$anon" -lt 5000000000 ] && [ "$(cat $CAP)" != 2 ]; then echo 2 > $CAP; echo "$(date +%T) anon=$((anon/1000000))MB build-j 2"; fi
  if [ "$cur" -gt 8000000000 ]; then
    echo 1500M > $CG/memory.reclaim 2>/dev/null
    echo "$(date +%T) cur=$((cur/1000000))MB anon=$((anon/1000000))MB after=$(($(cat $CG/memory.current)/1000000))MB"
  fi
  sleep 2
done
