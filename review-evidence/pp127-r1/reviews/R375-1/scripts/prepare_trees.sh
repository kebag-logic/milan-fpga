#!/bin/sh
# Extract the exact head and its base into the packet scratch area.
# usage: prepare_trees.sh <path-to-processor-clone>
set -eu
PKT=$(cd "$(dirname "$0")/.." && pwd)
CLONE=$1
mkdir -p "$PKT/scratch/head" "$PKT/scratch/base"
git -C "$CLONE" archive cf4e5c63ab12442c6c63d2bfe2bb64902674d55e | tar -x -C "$PKT/scratch/head"
git -C "$CLONE" archive 16be6768f710e79450aace277abacd6c2c3336e5 | tar -x -C "$PKT/scratch/base"
# then: python3 scripts/r375_run.py head,base
#       python3 scripts/r375_run.py all-mutants
#       python3 scripts/r375_author_mutants.py controls ; ... all
# (R375_VERILATOR selects the simulator wrapper; default is the pinned 5.050 one)
