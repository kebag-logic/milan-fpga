#!/bin/bash
# Start the final sweep (final30.sh, four native-shards units) once four ranges are free and MemAvailable is above
# 30 GB: three free 8-CPU ranges for shards 0, 1 and 3, and the first four CPUs of a fourth for shard 2, whose
# capture_coherence builds one datapath a CPU (four, or it runs out of memory). Checks every minute; a line per check
# that changes. usage: launch_sweep34.sh HEAD
set -u
H=$1 T=/data-2/milan/tmp/665s2b-a683zo L=$T/logs/launch-sweep34.txt
last=""
while true; do
    free=$(python3 $MANAGEMENT/2026-09-23/cpu_ranges.py show 2>&1 | tail -1)
    mem=$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo)
    ranges=$(python3 -c "
import re, sys
s = sys.argv[1]
r = []
for blk in re.findall(r'free16 \[(.*?)\]', s) + re.findall(r'half8 \[(.*?)\]', s):
    for x in re.findall(r\"'(\d+)-(\d+)'\", blk):
        a, b = int(x[0]), int(x[1])
        for lo in range(a, b + 1, 8):
            if lo + 7 <= b:
                r.append(f'{lo}-{lo + 7}')
print(' '.join(dict.fromkeys(r)))" "$free")
    n=$(echo $ranges | wc -w)
    now="free ranges: ${ranges:-none}; MemAvailable ${mem} GB"
    [ "$now" != "$last" ] && echo "$(date +%T) $now" >> $L && last=$now
    if [ "$n" -ge 4 ] && [ "$mem" -gt 30 ]; then
        set -- $ranges
        r3=$4; lo=${r3%-*}; s2="$lo-$((lo + 3))"
        echo "$(date +%T) launching: shard 0 $1, shard 1 $2, shard 2 $s2, shard 3 $3" >> $L
        bash $T/scripts/final30.sh $H $1 $2 $s2 $3
        echo "$(date +%T) final30.sh rc=$?" >> $L
        exit 0
    fi
    sleep 60
done
