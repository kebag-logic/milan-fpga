#!/bin/bash
# Wait for a free booked range and MemAvailable over 24 GB, then run cc_rerun.sh as its own unit on the range's first
# four CPUs (as the sweep placed shard 2). usage: cc_wait.sh SUITE BUDGET_S OUT
set -u
T=<scratch>
while true; do
    avail=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    if [ "$avail" -gt 25165824 ] && r=$(python3 <management>/2026-09-23/cpu_ranges.py pick); then
        a=${r%-*}; rr="$a-$((a + 3))"
        bash $T/scripts/unit.sh cc-rerun "$rr" 10G -- /bin/bash $T/scripts/cc_rerun.sh "$@"
        echo "$(date +%T) $1 re-run started as its own unit on $rr (MemAvailable $((avail / 1048576)) GB)" >> $T/logs/665s2b-a683ze-sweep.txt
        exit 0
    fi
    sleep 60
done
