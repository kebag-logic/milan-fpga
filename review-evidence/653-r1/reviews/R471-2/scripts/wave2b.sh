#!/bin/bash
# Wave 2b: rerun the wave-2 legs after giving each copy's submodules a local
# index (scripts/pp_srcs.py derives the processor list with git ls-files).
. "$(dirname "$0")/env.sh"
for c in m1 m2 m3 m4 m5 p1 basecrf; do
  run "leg_$c" make -C "$SCR/$c/tb/verilator/milan_dp" notify VERILATOR="$VERILATOR" VERILATOR_JOBS=3
done
wait
