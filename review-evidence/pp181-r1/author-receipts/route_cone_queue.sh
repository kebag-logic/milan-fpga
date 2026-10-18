#!/usr/bin/env bash
# routed-checkpoint cone reports, after route B: head, head+760, and the #760 lane's own route (read only)
S=<data>/tmp/pp181-a635
until grep -q ROUTE-DONE $S/route-head760/route.out 2>/dev/null; do sleep 30; done
. <home>/Xilinx/2026.1/Vivado/settings64.sh >/dev/null 2>&1 || true
for p in "head $S/route-head/work/ax7101/gateware/alinx_ax7101_route.dcp" \
         "head760 $S/route-head760/work/ax7101/gateware/alinx_ax7101_route.dcp" \
         "lane760 <data>/tmp/760-a630/route/work/ax7101/gateware/alinx_ax7101_route.dcp"; do
  set -- $p
  mkdir -p $S/cone/$1; cd $S/cone/$1
  flock -x $VIVADO_LOCK <home>/Xilinx/2026.1/Vivado/bin/vivado -mode batch -nojournal -log cone.log \
    -source $S/route_cone.tcl -tclargs "$2" > vivado.out 2>&1
  echo "rc=$?" > rc.txt
done
echo DONE > $S/cone/done.txt
