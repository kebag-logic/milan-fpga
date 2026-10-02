#!/bin/bash
# usage: wait.sh SECONDS NAME...  (foreground poll: returns when every NAME has an rc or SECONDS pass)
P=${PACKET:-$REVIEWS/pp143-r441-1-packet}
C=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
end=$(( $(date +%s) + $1 )); shift
while [ "$(date +%s)" -lt $end ]; do
  left=0; for n in "$@"; do [ -f "$P/receipts/$n/rc" ] || left=$((left+1)); done
  [ $left = 0 ] && break
  sleep 15
done
for n in "$@"; do printf '%s rc=%s wall=%s\n' "$n" "$(cat $P/receipts/$n/rc 2>/dev/null)" "$(cat $P/receipts/$n/wall 2>/dev/null)"; done
echo "anon=$(awk '/^anon /{print $2}' $C/memory.stat) peak=$(cat $C/memory.peak) oom_kill=$(awk '/oom_kill/{print $2}' $C/memory.events)"
