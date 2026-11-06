#!/bin/sh
# run_arm_top.sh <packet> <arm>: full srp_top end-to-end suite on one reviewer arm
P=$1; A=$2; W=$P/scratch/mut/$A; V=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
cd "$W/tb/srp_top" && timeout 570 make VERILATOR=$V run > "$P/receipts/mut/$A.top.log" 2>&1; rc=$?
echo "$A | top_rc=$rc | $(grep 'checks:' "$P/receipts/mut/$A.top.log" | tail -1) | $(grep -c '^FAIL' "$P/receipts/mut/$A.top.log") FAIL lines: $(grep '^FAIL' "$P/receipts/mut/$A.top.log" | cut -c1-60 | head -4 | tr '\n' ';')"
