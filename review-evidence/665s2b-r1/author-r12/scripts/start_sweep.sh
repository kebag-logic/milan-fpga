#!/bin/bash
# Wait for two free CPU ranges and MemAvailable above 30 GB, then start the four-shard sweep, each shard on half a range.
S=$MANAGEMENT/2026-09-23
O=$S/665s2b-a683o
T=$VALIDATION_STORAGE/665s2b-a683o
while :; do
    free=$(python3 $S/cpu_ranges.py show | sed -n "s/.*free16 \[\(.*\)\] free12.*/\1/p" | tr -d "'" )
    n=$(echo "$free" | tr ',' '\n' | grep -c -- '-')
    avail=$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)
    if [ "$n" -ge 2 ] && [ "$avail" -ge 30 ]; then
        A=$(echo "$free" | tr ',' '\n' | sed -n 1p | tr -d ' ') B=$(echo "$free" | tr ',' '\n' | sed -n 2p | tr -d ' ')
        a=${A%-*} b=${B%-*}
        exec python3 $S/native-shards.py 665s2b-o2 $O/receipts/native-spec.json $T/sweep2 4 $a-$((a+7)) $((a+8))-$((a+15)) $b-$((b+7)) $((b+8))-$((b+15))
    fi
    python3 -c 'import time; time.sleep(30)'
done
