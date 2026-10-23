#!/usr/bin/env bash
# Copy the round-7 Vivado bank's small reports into receipts/round7/<label>/,
# host paths and the host name stripped; a file of 200 KB or more (a log, a
# checkpoint) is recorded by sha256 and size only.
# usage: collect_vivado.sh <bank dir> <label>
set -uo pipefail
src=$1; label=$2
out=$MANAGEMENT/2026-09-23/632-a659/receipts/round7/$label
mkdir -p "$out"
strip() { sed -E -e 's#$VALIDATION_STORAGE/[A-Za-z0-9._/+-]*#<host path>#g' -e 's#$WORKSPACE_HOME/[A-Za-z0-9._/+-]*#<host path>#g' \
               -e 's#/tmp/[A-Za-z0-9._/+-]*#<tmp path>#g' -e 's#^(\| Host +: ).*#\1<host>#'; }
small() {  # <file> <name>
  [ -f "$1" ] || { echo "missing $1" >> "$out/missing.txt"; return; }
  if [ "$(stat -c %s "$1")" -lt 200000 ]; then strip < "$1" > "$out/$2"
  else printf '%s  %s bytes  %s\n' "$(sha256sum < "$1" | cut -d' ' -f1)" "$(stat -c %s "$1")" "$2" >> "$out/large_files.sha256"; fi
}
grep -E '^== |^GATE |rc=|DONE|^[0-9a-f]{40}$' "$src/bank.out" | strip > "$out/bank-steps.txt"
for e in route-1x1 ooc-1x1 ooc-8x8; do small "$src/$e-check.log" "$e-check.log"; done
g1=$src/w1/ax7101/gateware; o1=$src/w1/ax7101-ooc; r8=$src/w8/ax8x8-rtl; o8=$src/w8/ax8x8-ooc
small "$g1/alinx_ax7101_utilization_hierarchical_place.rpt" route_utilization_hierarchical_place.rpt
small "$g1/alinx_ax7101_utilization_hierarchical_synth.rpt" route_utilization_hierarchical_synth.rpt
small "$g1/alinx_ax7101_utilization_place.rpt" route_utilization_place.rpt
small "$g1/alinx_ax7101_route_status.rpt" route_status.rpt
small "$g1/baseline_scope_timing.tsv" route_scope_timing.tsv
small "$g1/baseline_timing.rpt" route_timing.rpt
small "$g1/baseline.log" route_vivado.log
small "$g1/baseline_images.json" route_baseline_images.json
for d in o1:ooc1x1 r8:rtl8x8 o8:ooc8x8; do
  dir=${d%%:*}; n=${d#*:}; eval "p=\$$dir"
  small "$p/baseline.log" "${n}_vivado.log"
  for r in "$p"/*utilization*.rpt "$p"/*timing*.rpt "$p"/baseline_images.json; do [ -f "$r" ] && small "$r" "${n}_$(basename "$r")"; done
done
for f in "$g1"/alinx_ax7101_route.dcp; do [ -f "$f" ] && printf '%s  %s bytes  %s\n' "$(sha256sum < "$f" | cut -d' ' -f1)" "$(stat -c %s "$f")" "$(basename "$f")" >> "$out/large_files.sha256"; done
# Vivado memory peaks and run minutes, per run
for d in "$g1:route-1x1" "$o1:ooc-1x1" "$r8:rtl-8x8" "$o8:ooc-8x8"; do
  p=${d%%:*}; n=${d#*:}
  [ -f "$p/baseline.log" ] || continue
  pk=$(grep -o 'peak = [0-9.]*' "$p/baseline.log" | awk '{print $3}' | sort -n | tail -1)
  printf '%s peak %s MB, log sha256 %s, %s bytes\n' "$n" "$pk" "$(sha256sum < "$p/baseline.log" | cut -d' ' -f1)" "$(stat -c %s "$p/baseline.log")" >> "$out/runs.txt"
done
ls "$out" | wc -l
