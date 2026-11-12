#!/usr/bin/env bash
# poll.sh: wait (at most ~9 min) for a new driver line or a nonzero step rc; then print the state.
W=<scratch>/gates/wf3
a=$(cat $W/drivers/fw.log $W/drivers/rest.log 2>/dev/null | wc -l)
bad() { for f in $W/logs/*.rc; do [ "$(cat $f)" != 0 ] && echo "NONZERO $(basename $f) $(cat $f)"; done; }
b0=$(bad | wc -l)
timeout 540 bash -c "until [ \$(cat $W/drivers/fw.log $W/drivers/rest.log 2>/dev/null | wc -l) -gt $a ]; do sleep 20; done"
cat $W/drivers/fw.log $W/drivers/rest.log | grep -E "end|done" | tail -4
bad
echo "mem $(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo) GB; load $(cut -d' ' -f1 /proc/loadavg); unit $(( $(cat /sys/fs/cgroup$(sed -n 's/^0:://p' /proc/self/cgroup)/memory.current) / 1048576 )) MB"
for r in base-1x1 final-1x1 base-8x8 final-8x8; do [ -f <scratch>/logs/s2-$r.rc ] && echo "s2 $r rc=$(cat <scratch>/logs/s2-$r.rc)"; done
echo "sweep: $(ls <scratch>/gates/sweep3/shard-*/logs 2>/dev/null | wc -l) files"
