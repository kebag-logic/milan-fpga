#!/bin/bash
# One line per leg of queue32: its unit, its group logs, PASS/FAIL results, the journal refusals; then the queue and memory.
T=/data-2/milan/tmp/665s2b-a683zo
for n in V32-1x1 GA8 GN8 GA1 GN1 GB8 GB1; do
    d=$T/builds/$n/results
    [ -d $d ] || { echo "$n -"; continue; }
    u=$(systemctl --user is-active milan-665s2b-a683zo-${n%%-*}.service 2>/dev/null)
    echo "$n unit=$u logs=$(ls $d/*.log 2>/dev/null | wc -l) pass=$(grep -l 'RESULT: PASS' $d/*.log 2>/dev/null | wc -l) fail=$(grep -l 'RESULT: FAIL' $d/*.log 2>/dev/null | wc -l) escaped=$(grep -l 'escaped the journal' $d/*.log 2>/dev/null | wc -l) rc=$(cat $T/logs/$n.log.rc 2>/dev/null)"
done
for c in $T/logs/ctl-*-da1869a3.log; do [ -f "$c" ] && echo "$(basename $c) $(tail -1 $c | cut -c1-80)"; done
echo "queue: $(awk '{print $1}' $T/logs/queue32.txt | tr '\n' ' ')"
tail -2 $T/logs/dispatch30.txt
grep MemAvailable /proc/meminfo
df -h /data-2 | tail -1
