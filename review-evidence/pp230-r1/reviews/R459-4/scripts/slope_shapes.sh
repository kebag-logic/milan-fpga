#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Run each checked-in slope control at every admission-suite shape separately
# (the suite's own `make` stops at the first failing shape).
# usage: slope_shapes.sh <tree> <work> <receipts> <jobs>; VERILATOR names the simulator.
set -u
TREE=$1 WORK=$2 REC=$3 JOBS=$4
mkdir -p "$WORK" "$REC"
export TREE WORK REC
for c in slope-stored-at-stage-2-index slope-stored-at-source-0 slope-store-source-0-only slope-read-source-0; do
  for n in 1 2 3 5 8; do echo "$c $n"; done
done | xargs -P "$JOBS" -L 1 sh -c '
  c=$0 n=$1 d="$WORK/$c-N$n"
  rm -rf "$d"; mkdir -p "$d/tb"
  cp -r "$TREE/hdl" "$d/hdl"; cp -r "$TREE/tb/srp_admission" "$TREE/tb/common" "$d/tb/"
  rm -rf "$d"/tb/srp_admission/obj_*
  (cd "$d" && git apply "$TREE/tb/srp_top/mutations/$c.patch") || { echo "$c N=$n: PATCH FAILED"; exit 0; }
  make -C "$d/tb/srp_admission" run N=$n > "$REC/$c-N$n.log" 2>&1
  echo "$c N=$n rc=$? $(grep -E "checks:" "$REC/$c-N$n.log" | tail -1)"
' | sort
