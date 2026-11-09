#!/usr/bin/env bash
# Wait (at most SECS, default 540) for every named gate's rc file: wait.sh [-t SECS] NAME...
PKT="$(cd "$(dirname "$0")/.." && pwd)"; R="$PKT/receipts"
secs=540; if [ "${1:-}" = -t ]; then secs=$2; shift 2; fi
end=$(( $(date +%s) + secs ))
while :; do
  left=0
  for n in "$@"; do [ -f "$R/$n.rc" ] || left=$((left+1)); done
  [ $left -eq 0 ] && break
  [ "$(date +%s)" -ge $end ] && break
  sleep 15
done
for n in "$@"; do
  if [ -f "$R/$n.rc" ]; then
    printf '%-28s rc=%s peakKB=%s\n' "$n" "$(cat "$R/$n.rc")" \
      "$(awk -F: '/Maximum resident/{gsub(/ /,"",$2);print $2}' "$R/$n.time" 2>/dev/null)"
  else
    printf '%-28s RUNNING (%s log lines)\n' "$n" "$(wc -l < "$R/$n.log" 2>/dev/null)"
  fi
done
cg=$(cut -d: -f3 /proc/self/cgroup); echo "unit mem now: $(( $(cat /sys/fs/cgroup$cg/memory.current) / 1048576 )) MiB, peak $(( $(cat /sys/fs/cgroup$cg/memory.peak 2>/dev/null || echo 0) / 1048576 )) MiB"
