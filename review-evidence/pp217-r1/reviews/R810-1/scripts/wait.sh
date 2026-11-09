#!/bin/bash
# usage: wait.sh <receipt-dir> <max-seconds> <name...> : polls until every name has an .rc or time runs out
R=$1; T=$2; shift 2
end=$(( $(date +%s) + T ))
while :; do
  left=0; for n in "$@"; do [ -f "$R/$n.rc" ] || left=$((left+1)); done
  [ $left -eq 0 ] && break
  [ $(date +%s) -ge $end ] && break
  sleep 15
done
cg=$(cut -d: -f3 /proc/self/cgroup)
echo "mem.current=$(cat /sys/fs/cgroup$cg/memory.current 2>/dev/null) peak=$(cat /sys/fs/cgroup$cg/memory.peak 2>/dev/null)"
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat $R/$n.rc 2>/dev/null || echo RUNNING)"; done
