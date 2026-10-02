#!/bin/bash
# usage: wait_rc.sh SECONDS TAG...  waits until every TAG's rc file exists or SECONDS pass
P=$REVIEWS/pp143-r440-1-packet
limit=$1; shift
deadline=$(( $(date +%s) + limit ))
until { all=1; for t in "$@"; do [ -e $P/receipts/runs/$t.rc ] || all=0; done; [ $all = 1 ]; } || [ $(date +%s) -ge $deadline ]; do
  sleep 5
done
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
for t in "$@"; do printf '%s rc=%s %s\n' $t "$(cat $P/receipts/runs/$t.rc 2>/dev/null || echo running)" "$(grep wall_s $P/receipts/runs/$t.meta 2>/dev/null)"; done
echo "peak=$(cat $cg/memory.peak) $(grep -E '^anon ' $cg/memory.stat) $(awk '/oom_kill /' $cg/memory.events)"
tail -1 $P/receipts/monitor.txt | cut -c1-80
