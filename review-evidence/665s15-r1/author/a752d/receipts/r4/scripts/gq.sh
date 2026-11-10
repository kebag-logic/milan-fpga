#!/bin/bash
# Book a free range for each queued job in turn (cpu_ranges.py pick), at most MAX of this lane's units at once.
# The queue is popped under its own lock, so a local runner can share it; the pick and the unit's start hold the
# lane's pick lock. usage: gq.sh MAX QUEUE_FILE   (each line: NAME|MEMORY_MAX|COMMAND)
set -u
T=$SCRATCH
PICK="python3 $MGMT/2026-09-23/cpu_ranges.py pick"
MAX=$1 Q=$2
active() { systemctl --user list-units 'milan-665s15-a752d-*' --no-legend --state=active --plain | grep -c '\.service'; }
pop() { ( flock 9; head -1 "$Q"; sed -i 1d "$Q" ) 9> "$Q.lock"; }
start_one() {
    exec 8> "$T/pick.lock"; flock 8
    range=$($PICK) || { flock -u 8; return 1; }
    line=$(pop)
    [ -z "$line" ] && { flock -u 8; return 2; }
    IFS='|' read -r name mem cmd <<< "$line"
    echo "$(date +%T) $name on $range: $cmd" >> $T/logs/gq.txt
    bash $T/scripts/gunit.sh "$name" "$range" "$mem" -- /bin/bash -c "source $T/scripts/env.sh; $cmd" >> $T/logs/gq.txt 2>&1
    sleep 5
    flock -u 8
    return 0
}
while true; do
    [ -s "$Q" ] || { echo "$(date +%T) $(basename $Q) empty" >> $T/logs/gq.txt; exit 0; }
    avail=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    if [ "$(active)" -lt "$MAX" ] && [ "$avail" -gt 20971520 ]; then
        start_one; rc=$?
        [ "$rc" = 2 ] && continue
        [ "$rc" = 0 ] && { sleep 20; continue; }
    fi
    sleep 60
done
