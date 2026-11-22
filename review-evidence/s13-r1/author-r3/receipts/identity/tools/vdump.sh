#!/usr/bin/env bash
# vdump.sh <route.dcp> <out-prefix>: dump.tcl over one routed checkpoint in Vivado batch mode (the gating recipe's
# Vivado, settings64.sh under the real HOME for its licence), then each dump file sorted in place.
set -u
D=$1; O=$2; S=<scratch>
source $S/bin/env.sh
export HOME=<home>
source <home>/Xilinx2/2026.1/Vivado/settings64.sh
mkdir -p "$(dirname "$O")"; cd "$(dirname "$O")"
vivado -mode batch -nojournal -nolog -source $S/bin/dump.tcl -tclargs "$D" "$O"; rc=$?
for x in cells nets; do LC_ALL=C sort -o "$O.$x" "$O.$x"; done
echo "vdump rc=$rc $(date -Iseconds)"; exit $rc
