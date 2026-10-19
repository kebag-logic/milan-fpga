#!/usr/bin/env bash
# usage: wait_jobs.sh <max seconds> <rc file>...  -- polls until every rc file exists or time runs out
P=$(cd "$(dirname "$0")/.." && pwd)   # the packet root
lim=$1; shift; t0=$(date +%s)
while :; do
  left=0; for f in "$@"; do [ -f "$f" ] || left=$((left+1)); done
  [ $left -eq 0 ] && { echo "all done"; break; }
  [ $(( $(date +%s) - t0 )) -ge $lim ] && { echo "$left pending"; break; }
  sleep 20
done
cg=$(cut -d: -f3 /proc/self/cgroup); echo "mem.current $(( $(cat /sys/fs/cgroup$cg/memory.current) / 1048576 )) MiB; peak $(( $(cat /sys/fs/cgroup$cg/memory.peak 2>/dev/null || echo 0) / 1048576 )) MiB"
for f in "$@"; do echo "$f: $(cat $f 2>/dev/null || echo pending)"; done
