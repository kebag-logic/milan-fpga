#!/usr/bin/env bash
# cdc.sh TAG DCP: cdc.tcl on one routed checkpoint, through the Vivado slot.
set -u
export HOME=<home> XILINXD_LICENSE_FILE=<home>/.Xilinx/Xilinx.lic
export PATH=/usr/local/bin:/usr/bin:/bin:<home>/Xilinx/2026.1/Vivado/bin
source <home>/Xilinx/2026.1/Vivado/settings64.sh
cd <scratch>/r5cdc
<management>/2026-09-23/vivado-slot.sh vivado -mode batch -nojournal -log cdc-$1.log -source cdc.tcl -tclargs $1 $2 > cdc-$1.out 2>&1
echo "cdc $1 rc=$? $(date +%T)"
