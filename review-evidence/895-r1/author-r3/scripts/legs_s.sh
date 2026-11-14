#!/bin/bash
# Start round 3's legs S-* at the head the clone r3/S holds (lane 895): arm A at both points (part 0's groups; the
# other parts queued for start_parts.sh, the splits of the Q-* legs), the answering-every-port, valid-destinations
# and answering-ports (group aecp) arms at both points, each its own unit on a range cpu_ranges.py picks.
set -u
M=$MANAGEMENT/2026-09-23
S1=$M/895-a775/scripts
T=/data-2/milan/tmp/895-a775
C=$T/r3/S
for spec in "S-A1:1x1:none:$(cat $T/builds/S-A1/part0.groups)" "S-A8:8x8:none:$(cat $T/builds/S-A8/part0.groups)" \
            "S-N8:8x8:answering-every-port" "S-N1:1x1:answering-every-port" "S-W1:1x1:valid-destinations" \
            "S-W8:8x8:valid-destinations" "S-B1:1x1:answering-ports:aecp" "S-B8:8x8:answering-ports:aecp"; do
  n=${spec%%:*}
  R=$(python3 $M/cpu_ranges.py pick) || { echo "no range for $n"; continue; }
  bash $S1/unit.sh "r3-leg-$n" "$R" 10G -- "CLONE=$C bash $S1/leg.sh '$spec'" >/dev/null 2>&1 && echo "$(date +%T) $n on $R"
  sleep 2
done
