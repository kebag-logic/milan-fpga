#!/bin/bash
# Book a free 16-CPU range (cpu_ranges.py pick) for each queued leg in turn, at most MAX of this lane's leg units at
# once beside its own unit (release lanes have CPU priority), each leg its own unit with JOBS=16 (leg.sh).
# usage: dispatch.sh MAX QUEUE_FILE   (each line: NAME CHECKOUT POINT GROUPS [run.py args...])
set -u
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
MAX=$1 Q=$2
active() { systemctl --user list-units 'milan-665s2b-a683u-*' --no-legend --state=active --plain | grep -c '\.service'; }
while true; do
    line=$(head -1 "$Q")
    [ -z "$line" ] && { echo "$(date +%T) queue empty" >> $T/logs/dispatch.txt; exit 0; }
    if [ "$(active)" -lt "$MAX" ] && range=$(python3 $MANAGEMENT/2026-09-23/cpu_ranges.py pick); then
        read -r name ck point groups extra <<< "$line"
        sed -i 1d "$Q"
        echo "$(date +%T) $name on $range ($(python3 $MANAGEMENT/2026-09-23/cpu_ranges.py show | tail -1))" >> $T/logs/dispatch.txt
        # shellcheck disable=SC2086
        bash $S/unit.sh "$name" "$range" 16G -- /usr/bin/env JOBS=16 /bin/bash $S/leg.sh "$T/$ck" "$name" "$point" "$groups" $extra >> $T/logs/dispatch.txt 2>&1
        sleep 30
    else
        sleep 60
    fi
done
