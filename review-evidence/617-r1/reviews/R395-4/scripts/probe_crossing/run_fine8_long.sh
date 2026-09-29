#!/usr/bin/env bash
# run_fine8_long.sh PPM LO HI FRAMES OUT [BIN]: run_fine8.sh with a chosen
# column count per engagement (64 sub-step phases x 4 quarter-cycle holds x
# offsets LO..HI), 8 phases in parallel.
set -u
ppm=$1; lo=$2; hi=$3; frames=$4; out=$5; bin=${6:-./obj_fine/Vcoherence_sim}
: > "$out"
for base in $(seq 0 8 63); do
  for k in $(seq $base $((base+7))); do
    "$bin" --probe "$ppm" "$lo" "$hi" 1 "$frames" 4 "$k" > "$out.$k" 2>&1 &
  done
  wait
  for k in $(seq $base $((base+7))); do cat "$out.$k" >> "$out"; rm -f "$out.$k"; done
done
