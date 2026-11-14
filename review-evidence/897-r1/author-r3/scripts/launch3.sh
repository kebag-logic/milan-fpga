#!/bin/bash
# Start one unit of lane 897 round 3 on a range cpu_ranges.py picks at that moment (never a range reused by hand), as
# its own transient unit (unit.sh). Waits (20 s steps) for a free range and MemAvailable above FLOOR GB.
# usage: launch3.sh NAME MEMORY_MAX FLOOR_GB CMD...   (log units/NAME.log, rc units/NAME.rc; a line in r3/logs/launch.txt)
set -u
NAME=$1 MEM=$2 FLOOR=$3; shift 3
T=/data-2/milan/tmp/897-a776
L=$T/r3/logs/launch.txt
while true; do
    r=$(python3 $MANAGEMENT/2026-09-23/cpu_ranges.py pick 2>/dev/null)
    mem=$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo)
    if [ -n "$r" ] && [ "$mem" -gt "$FLOOR" ]; then break; fi
    sleep 20
done
echo "$(date +%T) $NAME on $r (MemAvailable $mem GB) MemoryMax $MEM: $*" >> $L
bash $T/scripts/unit.sh "$NAME" "$r" "$MEM" "$T" -- "$@"
sleep 5
systemctl --user show -p MainPID --value "milan-897-a776-$NAME.service" | xargs -r -I{} taskset -cp {} >> $L 2>&1
