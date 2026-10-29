#!/bin/bash
# Under the exclusive Vivado lock (the caller holds it): the xvlog front-end gate, then the record mover out of
# context with the mailbox's recipe, from one checkout.
# usage: vivado_jobs.sh CHECKOUT WORK
set -u
S=$MANAGEMENT/2026-09-23/665s2b-a683m/scripts
C=$1 W=$2
mkdir -p "$W"
source $WORKSPACE_HOME/Xilinx/2026.1/Vivado/settings64.sh
bash $S/gate.sh "$C" "$W/xvlog_check.log" . python3 scripts/xvlog_gate.py --check
bash $S/dma_ooc.sh "$W" "$C"
echo "== vivado jobs done $(date -Is)"
