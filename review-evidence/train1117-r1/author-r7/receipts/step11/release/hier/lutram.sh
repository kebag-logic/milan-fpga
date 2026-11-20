#!/usr/bin/env bash
# lutram.sh: lutram.tcl on the candidate's and p11's routed release checkpoints, through the Vivado slot.
set -u
export HOME=<home> XILINXD_LICENSE_FILE=<home>/.Xilinx/Xilinx.lic
export PATH=/usr/local/bin:/usr/bin:/bin:<home>/Xilinx/2026.1/Vivado/bin
source <home>/Xilinx/2026.1/Vivado/settings64.sh
cd <scratch>/r5hier
<management>/2026-09-23/vivado-slot.sh vivado -mode batch -nojournal -log lutram.log -source lutram.tcl -tclargs \
  cand <scratch>/r5relC/work/ax7101-ExtraPostPlacementOpt/alinx_ax7101_route.dcp \
  p11 <scratch>/r5rel/work/ax7101/gateware/alinx_ax7101_route.dcp > lutram.out 2>&1
echo "lutram rc=$? $(date +%T)"
