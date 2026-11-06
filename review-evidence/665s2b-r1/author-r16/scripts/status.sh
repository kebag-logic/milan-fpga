#!/bin/bash
# This round's legs at a glance: each driver log's last line, the dispatcher's bookings, memory and free ranges.
T=$VALIDATION_STORAGE/665s2b-a683u
date +%T
for l in N-A8ss N-A8h N-B8h D-A8h D-B8 N-B1h D-A1 D-B1 D-NT8 RA-8 RA-1 AH-A8 P81-A8 TB-8; do
    f=$T/logs/$l.log
    [ -f "$f" ] || continue
    printf '%-7s %s | %s\n' "$l" "$(grep -c '^COMMAND .*native/Vsim' "$f") started" "$(tail -n 1 "$f" | cut -c1-110)"
done
grep -h ' on [0-9]' $T/logs/dispatch.txt | awk '$1 >= "06:57"' | tail -n 5
head -n 3 $T/queue2.txt | cut -c1-60
awk '/MemAvailable/ {print int($2/1048576) " GB available"}' /proc/meminfo
systemctl --user show milan-665s2b-a683u-r.service -p MemoryCurrent --value | awk '{print "own unit " int($1/1048576) " MB"}'
python3 $MANAGEMENT/2026-09-23/cpu_ranges.py show | tail -n 1
