#!/bin/bash
# The harness's controls and this round's labelled controls, one after another where the CPU generator may run.
# usage: controls.sh HEAD_CHECKOUT
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683o/scripts/env.sh
C=$1
T=$VALIDATION_STORAGE/665s2b-a683o
O=$MANAGEMENT/2026-09-23/665s2b-a683o
S=$O/scripts
one() { n=$1; shift; { echo "HEAD $(git -C "$C" rev-parse HEAD)"; echo "\$ $*"; (cd "$C" && python3 -B tb/verilator/ctrl_service_budget/run.py "$@"); echo "rc=$?"; } > "$T/logs/ctl-$n.log" 2>&1; }
one slow-adp-rx --point 1x1 --build-dir "$T/ctl/slow-rx" --fetch-l1 none --mutation slow-adp-rx --record-budget-findings
one slow-adp-shutdown --point 1x1 --build-dir "$T/ctl/slow-shut" --fetch-l1 none --variant shutdown-entry --mutation slow-adp-shutdown --record-budget-findings
one as-built --point 1x1 --build-dir "$T/ctl/asbuilt" --fetch-l1 none --cpu-regions as-built
one as-built-cached --point 1x1 --build-dir "$T/ctl/asbuilt-c" --cpu-regions as-built
$S/leg.sh $T/CT CT-A1 1x1 aecp,aecp-fanout,acmp-disc
$S/leg.sh $T/CT CT-A8 8x8 aecp,aecp-fanout,acmp-disc
$S/leg.sh $T/CP CP-A8 8x8 acmp-noresp
echo done > "$T/logs/controls.done"
