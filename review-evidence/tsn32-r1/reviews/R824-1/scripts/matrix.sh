#!/bin/bash
# The differential probe's matrix: mask widths x sink counts x modes x seeds. usage: matrix.sh SCRATCH OUT STEPS
S=$1 O=$2 STEPS=$3
: > "$O.jobs"
for spec in 16:1 16:8 16:16 32:1 32:8 32:32 33:1 33:8 33:32 33:33 64:33 64:63 64:64 255:255; do
  M=${spec%%:*} N=${spec##*:}
  for mode in "LIFT=0" "LIFT=1" "REENTER=1" "NOOPEN=1" "LIFT=1 REENTER=1 NOOPEN=1"; do
    for seed in 1 2 3 4 5 6 7 8; do
      st=$STEPS; [ "$N" -ge 63 ] && st=$((STEPS / 4))
      echo "env $mode SINKS=$N STEPS=$st SEED=$seed $S/dwalk-$M/dwalk" >> "$O.jobs"
    done
  done
done
xargs -P 12 -I{} sh -c '{} 2>&1 | head -2' < "$O.jobs" > "$O.txt"
echo $? > "$O.rc"
