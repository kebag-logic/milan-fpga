#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Run scripts/mutation_arm.py on a fresh export of the head, with the pinned
# Verilator (through scripts/bin) first on PATH.
# Usage: mutation_arm.sh <selection> <label>
set -eu
. "$(dirname "$0")/env.sh"
sel=$1; label=$2
tree="$SCRATCH/mut_tree_$label"; work="$SCRATCH/mut_work_$label"
rm -rf "$tree" "$work"; mkdir -p "$tree"
git -C "$CLONE" archive "$HEAD_SHA" | tar -x -C "$tree"
echo "# verilator: $(verilator --version); head $HEAD_SHA; selection $sel"
python3 "$PACKET/scripts/mutation_arm.py" "$tree" "$work" "$sel"
