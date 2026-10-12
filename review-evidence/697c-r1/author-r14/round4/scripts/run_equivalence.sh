#!/usr/bin/env bash
# Scratch: the memo equivalence check on one tree, pinned to CPUs 8-11.
# usage: run_equivalence.sh <tree> <log>
. $VALIDATION_STORAGE/697c-a583/r4/scripts/env.sh
taskset -c 8-11 python3 -B $VALIDATION_STORAGE/697c-a583/r4/scripts/memo_equivalence.py "$1" > "$2" 2>&1
echo "rc=$?" > "$2.rc"
