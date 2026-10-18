#!/usr/bin/env bash
S=<data>/tmp/pp181-a635
rm -rf $S/cone/head; mkdir -p $S/cone/head; cd $S/cone/head
flock -x $VIVADO_LOCK <home>/Xilinx/2026.1/Vivado/bin/vivado -mode batch -nojournal -log cone.log \
  -source $S/route_cone.tcl -tclargs $S/route-head/work/ax7101/gateware/alinx_ax7101_route.dcp > vivado.out 2>&1
echo "rc=$?" > rc.txt
