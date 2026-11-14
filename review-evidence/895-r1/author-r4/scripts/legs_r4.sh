#!/bin/bash
# Start round 4's legs R4-* at the merge the clone r4/L holds (lane 895): arm A at both points (part 0's groups, the
# build; parts 1-4 queued for start_parts_r4.sh), the answering-every-port, valid-destinations and answering-ports
# (group aecp) arms at both points, each its own unit on a range cpu_ranges.py picks (MemAvailable above 20 GB).
set -u
M=$MANAGEMENT/2026-09-23
S1=$M/895-a775/scripts
S4=$M/895-a775/round4/scripts
T=/data-2/milan/tmp/895-a775
C=$T/r4/L
for spec in "R4-A1:1x1:none:$(cat $T/builds/R4-A1/part0.groups)" "R4-A8:8x8:none:$(cat $T/builds/R4-A8/part0.groups)" \
            "R4-W1:1x1:valid-destinations" "R4-W8:8x8:valid-destinations" "R4-N1:1x1:answering-every-port" \
            "R4-N8:8x8:answering-every-port" "R4-B1:1x1:answering-ports:aecp" "R4-B8:8x8:answering-ports:aecp"; do
  n=${spec%%:*}
  [ -e "$T/legs/$n.rc" ] && { echo "$n already ran"; continue; }
  avail=$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo)
  [ "$avail" -gt 20 ] || { echo "MemAvailable $avail GB: stop"; break; }
  R=$(python3 $M/cpu_ranges.py pick) || { echo "no range for $n"; break; }
  bash $S4/unit.sh "leg-$n" "$R" 10G $C -- "CLONE=$C bash $S1/leg.sh '$spec'" >/dev/null 2>&1 && echo "$(date +%T) $n on $R"
  sleep 3
done
