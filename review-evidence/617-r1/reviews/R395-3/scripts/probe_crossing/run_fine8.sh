#!/usr/bin/env bash
# run_fine8.sh PPM LO HI OUT [BIN]: run_fine.sh with 8 phases in parallel (the
# review's job cap): 64 sub-step TDM phases x 4 quarter-cycle holds x offsets
# LO..HI, 300 columns each. BIN defaults to ./obj_fine/Vcoherence_sim.
set -u
ppm=$1; lo=$2; hi=$3; out=$4; bin=${5:-./obj_fine/Vcoherence_sim}
: > "$out"
for base in $(seq 0 8 63); do
  for k in $(seq $base $((base+7))); do
    "$bin" --probe "$ppm" "$lo" "$hi" 1 300 4 "$k" > "$out.$k" 2>&1 &
  done
  wait
  for k in $(seq $base $((base+7))); do cat "$out.$k" >> "$out"; rm -f "$out.$k"; done
done
