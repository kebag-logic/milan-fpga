#!/bin/bash
# poll2.sh [seconds]: wait up to the given time for a gate or shard to end (or memory to run low), then print the state
S=$VALIDATION_STORAGE/665s8-a758b; G=$S/gates
units="milan-665s8-a758b-shard0 milan-665s8-a758b-shard1 milan-665s8-a758b-shard2 milan-665s8-a758b-shard3 milan-a758b-gate-e1 milan-a758b-gate-e2 milan-a758b-gate-e3 milan-a758b-cc"
sig() { { cat $G/extra/jobs.txt $G/elaborate/logs/*gate_19-*.rc $S/cc-rerun/rc 2>/dev/null; for u in $units; do systemctl --user is-active $u 2>/dev/null; done; } | md5sum; }
mem() { awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo; }
s0=$(sig); end=$(( $(date +%s) + ${1:-500} ))
while [ $(date +%s) -lt $end ] && [ "$(sig)" = "$s0" ] && [ $(mem) -ge 22 ]; do sleep 10; done
date -u +%T; echo "MemAvailable $(mem) GB; load $(cut -d' ' -f1-3 /proc/loadavg)"
for u in $units; do printf '%s=%s ' ${u#milan-} $(systemctl --user is-active $u 2>/dev/null); done; echo
for k in 0 1 2 3; do printf 'shard%s %s logs; ' $k $(ls $S/sweep/shard-$k/logs 2>/dev/null | wc -l); done; echo
tail -4 $G/extra/jobs.txt
for f in $G/extra/logs/budget-1x1.log $G/extra/logs/budget-8x8.log $G/extra/logs/wire-8x8-none.log; do [ -f $f ] && echo "$(basename $f): $(grep -c COMMAND $f) commands, last: $(tail -1 $f | cut -c1-120)"; done
