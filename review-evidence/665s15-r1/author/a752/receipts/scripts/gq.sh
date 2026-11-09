#!/bin/bash
# Book a free range for each queued job in turn (cpu_ranges.py pick), at most MAX of this lane's units at once.
# The queue is popped under a lock, so a local runner can share it.
# usage: gq.sh MAX QUEUE_FILE   (each line: NAME|MEMORY_MAX|COMMAND, the command run by bash in its own unit)
set -u
T=<scratch>
PICK="python3 <management>/cpu_ranges.py pick"
MAX=$1 Q=$2
active() { systemctl --user list-units 'milan-665s15-a752-*' --no-legend --state=active --plain | grep -c '\.service'; }
pop() { ( flock 9; head -1 "$Q"; sed -i 1d "$Q" ) 9> "$Q.lock"; }
while true; do
    [ -s "$Q" ] || { echo "$(date +%T) $(basename $Q) empty" >> $T/logs/gq.txt; exit 0; }
    avail=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    if [ "$(active)" -lt "$MAX" ] && [ "$avail" -gt 20971520 ] && range=$($PICK); then
        line=$(pop)
        [ -z "$line" ] && continue
        IFS='|' read -r name mem cmd <<< "$line"
        echo "$(date +%T) $name on $range: $cmd" >> $T/logs/gq.txt
        bash $T/scripts/unit.sh "$name" "$range" "$mem" -- /bin/bash -c "$cmd" >> $T/logs/gq.txt 2>&1
        sleep 20
    else
        sleep 60
    fi
done
