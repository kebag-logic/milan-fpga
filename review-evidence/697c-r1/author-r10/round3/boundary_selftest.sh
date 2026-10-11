#!/usr/bin/env bash
# Scratch: the boundary gate's self-test on one tree, timed, its exit code beside its log.
# usage: boundary_selftest.sh <tree> <log>
set -u
tree=$1; log=$2
. $VALIDATION_STORAGE/697c-a583/round3/env.sh
cd "$tree" || exit 2
start=$(date +%s)
python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest > "$log" 2>&1
echo "rc=$? secs=$(( $(date +%s) - start ))" > "$log.rc"
