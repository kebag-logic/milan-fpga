#!/bin/bash
# Wait for a free 16-CPU range (cpu_ranges.py pick) with MemAvailable over 30 GB, then run the full sweep at HEAD as
# four native-shards units of four CPUs each in that range (sweep.sh), the shard holding capture_coherence on four.
# usage: sweep_when_free.sh HEAD OUT
set -u
H=$1 OUT=$2
T=$VALIDATION_STORAGE/665s2b-a683u
until [ "$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo)" -gt 30 ] && \
      r=$(python3 $MANAGEMENT/2026-09-23/cpu_ranges.py pick); do sleep 60; done
a=${r%-*}
echo "$(date +%T) sweep on $r: $a-$((a+3)) $((a+4))-$((a+7)) $((a+8))-$((a+11)) $((a+12))-$((a+15))" >> $T/logs/dispatch.txt
bash $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/sweep.sh "$H" "$OUT" "$a-$((a+3))" "$((a+4))-$((a+7))" \
  "$((a+8))-$((a+11))" "$((a+12))-$((a+15))" >> $T/logs/sweep.out 2>&1
echo "$(date +%T) sweep launcher rc=$?" >> $T/logs/dispatch.txt
