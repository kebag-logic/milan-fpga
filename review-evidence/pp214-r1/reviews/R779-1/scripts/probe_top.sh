#!/bin/bash
# usage: probe_top.sh <name> <group>: run one tb/srp_top group on a planted tree
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
export PATH=${VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}:$PATH
n=$1; g=$2; t=$PKT/scratch/mut/$n; l=$PKT/scratch/logs/probe-$n.top-${g:-all}.log
sed -i 's/--build -j 0/--build -j 2/' "$t/tb/srp_top/Makefile"
make -C "$t/tb/srp_top" run ${g:+RUN_ARGS=$g} > "$l" 2>&1; rc=$?
printf '%s group=%s rc=%s %s first=%s\n' "$n" "$g" "$rc" "$(grep -E '^[0-9]+ checks' "$l" | tail -1)" "$(grep -m1 '^FAIL' "$l" | cut -c1-90)" >> "$PKT/receipts/probes-srp_top.txt"
