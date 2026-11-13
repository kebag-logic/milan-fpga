#!/bin/bash
# One line per unit of queue 33: its unit state, its group logs and PASS/FAIL results, its rc; then the queue, memory
# and disk.
T=/data-2/milan/tmp/665s2b-a683zo
for n in F-GA8 F-GN8 F-GB8 S-GA1 S-GN1 S-GB1; do
    d=$T/builds/$n
    u=$(systemctl --user is-active milan-665s2b-a683zo-$n.service 2>/dev/null)
    logs=$(ls $d/results*/*.log 2>/dev/null | wc -l)
    pass=$(grep -l 'RESULT: PASS' $d/results*/*.log 2>/dev/null | wc -l)
    fail=$(grep -l 'RESULT: FAIL' $d/results*/*.log 2>/dev/null | wc -l)
    echo "$n unit=$u logs=$logs pass=$pass fail=$fail rc=$(cat $T/logs/rc/$n.rc 2>/dev/null)"
done
for h in F-GA8-h1 F-GA8-h2; do echo "$h unit=$(systemctl --user is-active milan-665s2b-a683zo-$h.service 2>/dev/null) rc=$(cat $T/logs/rc/$h.rc 2>/dev/null)"; done
for c in $T/logs/ctl-*-6c284a97.log; do [ -f "$c" ] && echo "$(basename $c .log) $(grep -E '^CONTROL|^ESCAPED' $c | cut -c1-90) $(tail -1 $c | cut -c1-40)"; done
echo "queue: $(awk '{print $1}' $T/logs/queue33.txt | tr '\n' ' ')"
tail -2 $T/logs/dispatch30.txt
grep MemAvailable /proc/meminfo
df -h /data-2 | tail -1
