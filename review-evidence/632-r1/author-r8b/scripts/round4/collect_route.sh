#!/usr/bin/env bash
# Copy a route-1x1 run's small reports into receipts/<label>/, host paths and
# the host name stripped. usage: collect_route.sh <route dir> <label>
set -euo pipefail
src=$1; label=$2
out=$MANAGEMENT/2026-09-23/632-a659/receipts/round4/$label
gw=$src/work/ax7101/gateware
mkdir -p "$out"
strip() { sed -E -e 's#$VALIDATION_STORAGE/[^ ]*/gateware#<work>/gateware#g' -e 's#$VALIDATION_STORAGE/[^ ]*#<host path>#g' \
               -e 's#^(\| Host +: ).*#\1<host>#'; }
[ -f "$src/route-1x1-check.log" ] && strip < "$src/route-1x1-check.log" > "$out/route-1x1-check.log"
# the head, the processor and gPTP submodule heads, timestamps and verdicts
grep -E '^[0-9a-f]{40}$|^20[0-9-]+T|rc=|DONE' "$src/route.out" > "$out/route-steps.txt" || true
strip < "$gw/alinx_ax7101_utilization_hierarchical_place.rpt" > "$out/utilization_hierarchical_place.rpt"
strip < "$gw/alinx_ax7101_route_status.rpt" > "$out/route_status.rpt"
cp "$gw/baseline_scope_timing.tsv" "$out/scope_timing.tsv"
# the worst setup path's header
n=$(grep -n -m1 'Slack (MET)\|Slack (VIOLATED)' "$gw/baseline_timing.rpt" | cut -d: -f1)
w=$(awk '/Slack \((MET|VIOLATED)\) :.*required time - arrival time/{v=$4+0; if(min==""||v<min){min=v;l=NR}} END{print l}' "$gw/baseline_timing.rpt")
sed -n "${w},$((w+12))p" "$gw/baseline_timing.rpt" | strip > "$out/worst_setup_path.txt"
: "$n"
sha256sum "$gw/alinx_ax7101_route.dcp" | sed -E 's#  .*/#  #' > "$out/route_dcp.sha256"
stat -c '%s bytes %n' "$gw/alinx_ax7101_route.dcp" | sed -E 's# /.*/# #' >> "$out/route_dcp.sha256"
ls -la "$out"
