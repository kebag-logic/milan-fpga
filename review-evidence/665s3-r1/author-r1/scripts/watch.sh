#!/bin/bash
# Wait up to $1 seconds (default 540) while this lane's gate units run; return early when one ends or memory is low.
# Prints each unit's state and memory, MemAvailable, and each gate log's last result line.
set -u
W=$VALIDATION_STORAGE/665s3-a697b
limit=${1:-540}
units() { systemctl --user list-units 'milan-665s3-a697b-*' --no-legend --plain --all | awk '{print $1}' | sort; }
before=$(units | tr '\n' ' ')
start=$(date +%s)
while :; do
    now=$(units | tr '\n' ' ')
    avail=$(awk '/MemAvailable/ {print int($2 / 1048576)}' /proc/meminfo)
    [ "$now" != "$before" ] && break
    [ "$avail" -lt 15 ] && { echo "LOW MEMORY: ${avail} GB"; break; }
    [ $(( $(date +%s) - start )) -ge "$limit" ] && break
    sleep 15
done
echo "MemAvailable ${avail} GB after $(( $(date +%s) - start )) s"
for u in $(units); do
    printf '%s %s cur=%sM peak=%sM\n' "$u" "$(systemctl --user show "$u" -p ActiveState --value)" \
        "$(( $(systemctl --user show "$u" -p MemoryCurrent --value 2>/dev/null | sed 's/\[not set\]/0/;s/^$/0/') / 1048576 ))" \
        "$(( $(systemctl --user show "$u" -p MemoryPeak --value 2>/dev/null | sed 's/\[not set\]/0/;s/^$/0/') / 1048576 ))"
done
for f in "$W"/gates/*.log; do
    printf '%s: %s\n' "$(basename "$f")" "$(grep -E '^rc=|PASS|FAIL|plants caught' "$f" | tail -2 | tr '\n' ' ' | cut -c1-150)"
done
