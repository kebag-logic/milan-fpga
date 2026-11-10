#!/bin/sh
# usage: run_reviewer_scripts.sh TREE OUT -- both reviewers' scripts, unchanged, from their packets, at TREE; each with
# its own log and rc. Writes OUT/done last. (R811-1's env.sh sets T, so the tree is held in TREE_AT.)
TREE_AT=$1 O=$2
P1=$HOME/milan-fpga-management/2026-09-23/tsn31-r811-1 P2=$HOME/milan-fpga-management/2026-09-23/tsn31-r812-1
export TOOLS=$TOOLS TMPDIR=$SCRATCH/tmp
rm -rf "$O"; mkdir -p "$O"
( . "$P1/env.sh"; python3 "$P1/scripts/plants.py" "$TREE_AT" "$O/r811-plants" 8 > "$O/r811-plants.log" 2>&1; echo $? > "$O/r811-plants.rc" ) &
( sh "$P1/scripts/survivors_full_ctest.sh" "$TREE_AT" "$O/r811-survivors" > "$O/r811-survivors.log" 2>&1; echo $? > "$O/r811-survivors.rc" ) &
( bash "$P2/scripts/run_wide_gaps.sh" "$P2" "$TREE_AT" "$O/r812-wide-gaps" > "$O/r812-wide-gaps.log" 2>&1; echo $? > "$O/r812-wide-gaps.rc" ) &
wait
echo done > "$O/done"
