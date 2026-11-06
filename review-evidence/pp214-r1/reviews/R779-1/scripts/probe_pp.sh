#!/bin/bash
# usage: probe_pp.sh <name>: run tb/pp_top on a planted tree
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
export PATH=${VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}:$PATH
n=$1; t=$PKT/scratch/mut/$n; l=$PKT/scratch/logs/probe-$n.pp.log
[ -d "$t/tb/pp_top" ] || rsync -a --exclude 'obj_*' "$PKT/scratch/head/tb/pp_top" "$t/tb/"
sed -i 's/--build -j 0/--build -j 2/' "$t/tb/pp_top/Makefile"
make -C "$t/tb/pp_top" > "$l" 2>&1; rc=$?
printf '%s pp_top rc=%s %s first=%s\n' "$n" "$rc" "$(grep -E 'checks' "$l" | tail -1 | cut -c1-70)" "$(grep -m1 '^FAIL' "$l" | cut -c1-90)" >> "$PKT/receipts/probes-pp_top.txt"
