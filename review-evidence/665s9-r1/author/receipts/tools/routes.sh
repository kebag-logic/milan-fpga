#!/usr/bin/env bash
# routes.sh: the integrated split route, then the all-fabric endpoint route, one at a time, each in its gateware dir.
set -u
S=<scratch>
source <home>/Xilinx/2026.1/Vivado/settings64.sh
for r in split fabric; do
  g=$S/route/$r/gateware
  ( cd "$g" && date -Iseconds > route.start && vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log > vivado.out 2>&1; echo $? > route.rc; date -Iseconds > route.end )
  echo "$r rc=$(cat $g/route.rc)"
done
echo done > $S/route/ROUTES_DONE
