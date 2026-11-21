#!/usr/bin/env bash
# bramdump.sh <out-dir> <label-a> <dcp-a> <label-b> <dcp-b>: bramdump.tcl over two routed checkpoints in Vivado batch.
set -u
O=$1; mkdir -p "$O"; cd "$O"
source <scratch>/bin/env.sh; export HOME=<home>
source <home>/Xilinx2/2026.1/Vivado/settings64.sh
vivado -mode batch -nojournal -nolog -source <scratch>/bin/bramdump.tcl -tclargs "$3" "$O/$2.bram"; ra=$?
vivado -mode batch -nojournal -nolog -source <scratch>/bin/bramdump.tcl -tclargs "$5" "$O/$4.bram"; rb=$?
echo "bramdump rc=$ra,$rb"; [ $ra = 0 ] && [ $rb = 0 ]
