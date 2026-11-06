#!/bin/bash
# usage: probe_suite.sh <name>: run tb/srp_encoder on a planted tree and report the verdict
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
export PATH=${VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}:$PATH
n=$1; t=$PKT/scratch/mut/$n; l=$PKT/scratch/logs/probe-$n.enc.log
sed -i 's/--build -j 0/--build -j 2/' "$t/tb/srp_encoder/Makefile"
make -C "$t/tb/srp_encoder" > "$l" 2>&1; rc=$?
printf '%s rc=%s %s first=%s\n' "$n" "$rc" "$(grep -E '^[0-9]+ checks' "$l" | tail -1)" "$(grep -m1 '^FAIL' "$l" | cut -c1-90)"
