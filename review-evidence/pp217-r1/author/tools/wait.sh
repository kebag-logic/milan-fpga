#!/usr/bin/env bash
# wait.sh <max_s> <rcfile>...: return when every rc file exists or after max_s; prints the states and memory
set -u
max=$1; shift
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
end=$(( $(date +%s) + max ))
while :; do
  all=1; for f in "$@"; do [ -f "$f" ] || all=0; done
  [ $all = 1 ] && break
  [ "$(date +%s)" -ge "$end" ] && break
  sleep 10
done
for f in "$@"; do if [ -f "$f" ]; then echo "$f rc=$(cat "$f")"; else echo "$f running"; fi; done
echo "mem $(( $(cat $CG/memory.current) / 1000000 )) MB peak $(( $(cat $CG/memory.peak 2>/dev/null || echo 0) / 1000000 )) MB avail $(awk '/MemAvailable/{print int($2/1000000)}' /proc/meminfo) GB"
