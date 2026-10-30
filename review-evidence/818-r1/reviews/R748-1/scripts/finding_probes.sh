#!/usr/bin/env bash
# Reproduce the review's findings on scratch copies of the recorded dev route set (made by route_probes.py).
# usage: finding_probes.sh <clone> <packet>
set -u
C=$1 P=$2 G=$C/syn/ooc/pp_resource_gate.py O=$P/receipts/finding-probes; mkdir -p "$O"
R=$P/scratch/probes/dev-control
# F1: the MARK_II_AREA_PLAN.md mapping procedure's record command, verbatim but for paths.
cp "$C/syn/ooc/pp_resource_baseline.json" "$P/scratch/scratch_baseline.json"
rc=0; python3 -B "$G" record "$R/ax7101/gateware" --endpoint route-1x1 --baseline "$P/scratch/scratch_baseline.json" --write \
  > "$O/F1-mark2-record-verbatim.log" 2>&1 || rc=$?; echo "F1 verbatim rc=$rc" | tee "$O/rc.txt"
rc=0; python3 -B "$G" record "$R/ax7101/gateware" --endpoint route-1x1 --shipping-selection --baseline "$P/scratch/scratch_baseline.json" --write \
  > "$O/F1-mark2-record-marked.log" 2>&1 || rc=$?; echo "F1 with --shipping-selection rc=$rc" | tee -a "$O/rc.txt"
# F2: a floor miss that is also a fall of more than 0.25 ns prints no WARNING (route_probes best-wns-one-corner).
B=$P/receipts/route-probes/best-wns-one-corner.log
echo "F2 best-wns-one-corner: WNS line: $(grep '^WNS_ns' "$B")" | tee -a "$O/rc.txt"
echo "F2 WARNING lines: $(grep -c WARNING "$B")" | tee -a "$O/rc.txt"
