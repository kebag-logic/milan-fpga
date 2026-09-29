#!/usr/bin/env bash
# run_fine.sh PPM LO HI OUT : 64 sub-step TDM phases x 4 quarter-cycle holds x
# offsets LO..HI, 300 columns each; 4 phases in parallel at a time.
set -u
ppm=$1; lo=$2; hi=$3; out=$4
: > "$out"
for base in $(seq 0 4 63); do
  for k in $base $((base+1)) $((base+2)) $((base+3)); do
    ./obj_fine/Vcoherence_sim --probe "$ppm" "$lo" "$hi" 1 300 4 "$k" > "$out.$k" 2>&1 &
  done
  wait
  for k in $base $((base+1)) $((base+2)) $((base+3)); do cat "$out.$k" >> "$out"; rm -f "$out.$k"; done
done
