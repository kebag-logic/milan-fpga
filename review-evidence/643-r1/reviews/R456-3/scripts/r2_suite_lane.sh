#!/bin/bash
# R456-2: in one scratch tree, the published boundary diagnostic exactly as
# TESTING.md documents it (from inside the suite directory), then the suite's
# default target cold-ish (the diagnostic's own tdm8render-build is reused).
# Usage: r2_suite_lane.sh PACKET TREE TAG
set -u
P=$1; T=$2; TAG=$3; R=$P/receipts/suites; mkdir -p $R
VL=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
cd $T/tb/verilator/milan_dp_render || exit 9
t0=$(date +%s)
make tdm8render-law-boundary VERILATOR=$VL VERILATOR_JOBS=3 LAW_BOUNDARY_JOBS=${LBJ:-5} > $R/bnd-$TAG.log 2>&1
echo "rc=$? wall=$(( $(date +%s) - t0 ))" > $R/bnd-$TAG.rc
t0=$(date +%s)
make VERILATOR=$VL VERILATOR_JOBS=3 > $R/suite-$TAG.log 2>&1
echo "rc=$? wall=$(( $(date +%s) - t0 ))" > $R/suite-$TAG.rc
