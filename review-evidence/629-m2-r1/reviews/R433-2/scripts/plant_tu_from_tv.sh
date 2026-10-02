#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer probe (R433-1): the design-named mutant of the meter suite's
# "History restarts" row, "tu taken from the tv net (the CRF wiring)", planted
# at the root (the only place the meter's tu input is wired), then the root
# suite's three clean legs run on it. An escape is all three legs passing.
# Usage (from a full checkout of the head with its submodules):
#   plant_tu_from_tv.sh <checkout> <outdir>   (VERILATOR may name the pinned binary)
set -eu
T=$(cd "$1" && pwd); O=$(mkdir -p "$2" && cd "$2" && pwd)
MUT="$O/mut_tu_from_tv_milan_datapath.sv"
python3 - "$T/hdl/milan/milan_datapath.sv" "$MUT" <<'EOF'
import sys
src = open(sys.argv[1]).read()
a = "      .tu_i          (avtprx_tu_bit),"
assert src.count(a) == 1, "anchor must occur exactly once"
open(sys.argv[2], "w").write(src.replace(a, "      .tu_i          (avtprx_tv_bit),"))
EOF
cd "$T/tb/verilator/milan_dp_mclk"
make mclk-build VERILATOR="${VERILATOR:-verilator}" VERILATOR_JOBS=8 \
     MUT_DP_SRC="$MUT" MCLK_MDIR=obj_tu > "$O/mut_tu_build.log" 2>&1
grep -q "mut_tu_from_tv_milan_datapath.sv" "$O/mut_tu_build.log"
for leg in A B C; do
  case $leg in A) arg="";; B) arg="--b";; C) arg="--c";; esac
  ( ./obj_tu/Vmilan_dp_mclk $arg > "$O/mut_tu_from_tv_leg$leg.log" 2>&1;
    echo "leg$leg rc=$?" >> "$O/mut_tu_from_tv_leg$leg.log" ) &
done
wait
tail -n 3 "$O"/mut_tu_from_tv_leg*.log
