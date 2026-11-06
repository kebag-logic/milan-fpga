#!/usr/bin/env bash
# camp_h.sh <head>: the milan_dp campaigns at <head> on a clean clone: unb-mutants, arm 1 read by name, gsi-mutants.
set -u
H=$1; S=<scratch>; W=$S/h-camp-wt; G=$S/camp-logs-$H
export MAKEFLAGS="-j16 --no-print-directory"
bash $S/tools/gates.sh "$H" "$W" "$G" \
  "unb_mutants=make -C tb/verilator/milan_dp unb-mutants" \
  "unb_arm1_names=python3 -B $S/tools/arm_failures.py $W/tb/verilator/milan_dp 1 $G/unb_arm1_leg.log" \
  "anchor_scan=python3 -B $S/tools/anchor_scan.py $W" \
  "gsi_mutants=make -C tb/verilator/milan_dp gsi-mutants"
