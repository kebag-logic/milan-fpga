#!/usr/bin/env bash
# route_one.sh <split|fabric>: one integrated route in its exported gateware dir; writes route.rc, route.start, route.end.
set -u
S=<scratch>; r=$1
source <home>/Xilinx/2026.1/Vivado/settings64.sh
g=$S/route/$r/gateware
cd "$g" || exit 3
date -Iseconds > route.start
vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log > vivado.out 2>&1
echo $? > route.rc
date -Iseconds > route.end
echo "$r rc=$(cat route.rc)"
