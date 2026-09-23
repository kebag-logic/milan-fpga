#!/bin/bash
# Run the donor engine suite's own mutation arm (tb/verilator/engine/mutants.py)
# on a disposable export of the donor tree at REV, pinned Verilator first on
# PATH. The published receipt donor-engine-mutants-head.log was produced by
# the same command run inside the export donor_copy.sh made for the engine run.
# Usage: donor_mutants.sh <label> <rev>
set -euo pipefail
. "$(dirname "$0")/env.sh"
label=$1; rev=$2
dst=$PACKET/scratch/donor-$label
rm -rf "$dst"; mkdir -p "$dst"
git -C "$CLONE" archive "$rev" | tar -x -C "$dst"
cd "$dst/tb/verilator/engine"
python3 mutants.py
