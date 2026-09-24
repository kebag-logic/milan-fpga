#!/usr/bin/env bash
# Run one suite target on an extracted tree. Usage: run_one.sh <tree> <logdir> <name> <tbdir> <target>
# PIN_VERILATOR must point at Verilator 5.050 (the CI pin).
set -uo pipefail
tree=$1; logs=$2; name=$3; dir=$4; tgt=$5
: "${PIN_VERILATOR:?set PIN_VERILATOR}"
mkdir -p "$logs"
start=$(date +%s)
( cd "$tree/$dir" && make VERILATOR="$PIN_VERILATOR" "$tgt" ) >"$logs/$name.log" 2>&1
rc=$?
tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$logs/$name.log" | tail -1)
echo "$name exit=$rc secs=$(( $(date +%s) - start )) | $tally" | tee "$logs/$name.exit"
