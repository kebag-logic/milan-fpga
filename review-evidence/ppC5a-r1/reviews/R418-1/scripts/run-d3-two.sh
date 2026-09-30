#!/usr/bin/env bash
# The two D3 controls whose counts moved, at the head and with the kill tied off.
# Usage: run-d3-two.sh <export-dir> <packet-dir>
set -u
EXP=$1; PKT=$2
export PATH="$PKT/scratch/bin:$PATH" TMPDIR="$PKT/scratch/tmp"
mkdir -p "$TMPDIR"
cd "$EXP" && python3 tb/pp_top/d3_mutants.py --output "$PKT/scratch/d3-logs-head" --verilator verilator --jobs 2 --only hold_released_at_go dispatch_not_held
echo "head rc=$?"
git apply tb/pp_top/mutations/dl-kill-tied-off.patch && echo "applied dl-kill-tied-off to the scratch export"
python3 tb/pp_top/d3_mutants.py --output "$PKT/scratch/d3-logs-tied" --verilator verilator --jobs 2 --only hold_released_at_go dispatch_not_held
echo "tied-off rc=$?"
