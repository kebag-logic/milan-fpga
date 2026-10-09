#!/usr/bin/env bash
# Usage: ooc_run.sh NAME  - OOC 1x1 synthesis of scratch/ooc/NAME/src with the tree's own recipe
set -u
P=$REVIEWS/pp168-r552-1-packet; n=$1
cd $P/scratch/ooc/$n/build || exit 2
$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin/vivado -mode batch -nojournal -log ooc.log \
  -source $P/scratch/ooc/$n/src/syn/ooc/protocol_processor_ooc.tcl -tclargs $P/scratch/ooc/$n/src 1 1
