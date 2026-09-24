#!/usr/bin/env bash
# run_suite.sh <tree> <suite> [target] : build+run one tb suite with the pinned
# simulator; prints the tally line and every FAIL line; exit = make's status
set -uo pipefail
V=${VERILATOR:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator}
tree=$1; suite=$2; tgt=${3:-run}
log=$(mktemp)
(cd "$tree/tb/$suite" && make VERILATOR="$V" "$tgt") >"$log" 2>&1; rc=$?
grep -E 'FAIL' "$log" | grep -v '^%Warning' | head -60
grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$log" | tail -3
grep -E '^%Error' "$log" | head -5
echo "exit=$rc"
rm -f "$log"; exit $rc
