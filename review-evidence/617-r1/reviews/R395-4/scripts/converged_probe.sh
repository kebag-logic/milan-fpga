#!/usr/bin/env bash
# The committed CRF-settle placements (near: 0 at negative rates, +8 at positive;
# far: 256 further to that side), 150,000 columns each, at +/-100 and +/-150 ppm,
# 8 at once, through the round-3 probe build (scripts/probe_crossing, BUILD.txt)
# of the exact head. Usage: converged_probe.sh <probe build dir> <outdir>
set -u
B=$1; O=$2; cd "$B"
for ppm in -150 150 -100 100; do
  if [ "$ppm" -lt 0 ]; then offs="0 -256"; else offs="8 264"; fi
  for off in $offs; do
    timeout 570 ./obj_probe/Vcoherence_sim --probe "$ppm" "$off" "$off" 256 150000 1 > "$O/conv${ppm}_${off}.log" 2>&1 &
  done
done
wait
