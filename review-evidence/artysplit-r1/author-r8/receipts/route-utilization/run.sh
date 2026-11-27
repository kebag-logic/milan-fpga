#!/bin/bash
# Report post-route utilization of round 7's and round 6's routed checkpoints, one at a time.
set -eu
R=$VALIDATION_STORAGE/r8/route-util
for pair in "r7:$VALIDATION_STORAGE/r7/images/AltSpreadLogic_high/gateware" "r6:$VALIDATION_STORAGE/r6g/images/AltSpreadLogic_high/gateware"; do
  tag=${pair%%:*}; dir=${pair#*:}
  sha256sum $dir/digilent_arty_route.dcp $dir/digilent_arty.bit > $R/$tag-identity.txt
  mkdir -p $R/$tag && cd $R/$tag
  VIVADO_SLOTS=2 VIVADO_MIN_GB=20 nice -n 19 $LANE_TOOLS/vivado-slot.sh bash -c 'source $XILINX/2026.1/Vivado/settings64.sh; exec vivado -mode batch -nojournal -nolog -source "$1" -tclargs "$2" "$3"' x $R/report.tcl $dir/digilent_arty_route.dcp $R/$tag-route-utilization.rpt > $R/$tag-vivado.log 2>&1
  echo "$tag rc=$?"
done
