#!/usr/bin/env bash
# The lane's campaign at the exact head, from a disposable export; temp trees in scratch.
# Usage: run-aecp-mutants.sh <clone> <head-sha> <packet-dir> [--only a,b]
set -u
CLONE=$1; HEAD=$2; PKT=$3; shift 3
EXP=$PKT/scratch/mutants-src
rm -rf "$EXP"; mkdir -p "$EXP" "$PKT/scratch/tmp" "$PKT/receipts"
git -C "$CLONE" archive "$HEAD" | tar -x -C "$EXP"
sed -i 's/--build -j 0/--build -j 8/' "$EXP/tb/pp_top/Makefile" "$EXP/tb/ucpu/Makefile"
export PATH="$PKT/scratch/bin:$PATH" TMPDIR="$PKT/scratch/tmp"
verilator --version
cd "$EXP/tb/pp_top" && python3 aecp_mutants.py --output "$PKT/scratch/mutant-logs" "$@"
