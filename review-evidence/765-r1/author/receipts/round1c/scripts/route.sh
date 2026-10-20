#!/bin/bash
# Route the head export; started as: setsid nohup flock $VIVADO_LOCK route.sh
export PATH=<home>/Xilinx/2026.1/Vivado/bin:$PATH
W=<scratch>/round1c/route-head
G=$W/work/ax7101/gateware
date -Is > $W/route.start
cd "$G" && vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log > $W/route.out 2>&1
echo "rc=$?" > $W/route.rc
date -Is > $W/route.end
