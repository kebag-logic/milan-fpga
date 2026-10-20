#!/bin/bash
# Route the round-1b export; record rc and times. Started under the exclusive Vivado lock.
export PATH=<home>/Xilinx/2026.1/Vivado/bin:$PATH
W=<scratch>/route-r1b
G=$W/work/ax7101/gateware
date -Is > $W/route.start
cd "$G" && vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log > $W/route.out 2>&1
echo "rc=$?" > $W/route.rc
date -Is > $W/route.end
