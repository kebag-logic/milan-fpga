#!/usr/bin/env bash
# route_directive.sh <directive>: implementation of the split route's synthesis checkpoint with another placement
# directive (#818's best of three; docs/testing/PP_SHADOW_BASELINE_RECIPE.md, Integrated measurements).
set -u
S=<scratch>; d=$1
source <home>/Xilinx/2026.1/Vivado/settings64.sh
cd $S/route/split-$d || exit 3
date -Iseconds > route.start
vivado -mode batch -source baseline_implementation.tcl -nojournal -log baseline.log > vivado.out 2>&1
echo $? > route.rc
date -Iseconds > route.end
