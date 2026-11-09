#!/bin/bash
# The lane gates left after the reboot (test_builder onward), one log and one rc per gate, never piped, on a fresh clean clone.
# usage: lane_gates.sh COMMIT TAG
set -u
H=$1 TAG=$2
S=$SCRATCH/scripts
T=$SCRATCH
W=$T/lane-wt-${TAG}r
G=$T/gates-out/lane-${TAG}r
mkdir -p "$G"
[ -d "$W" ] || bash "$S/clone.sh" "$W" "$H" > "$G/clone.log" 2>&1
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
. "$S/env.sh"
export TMPDIR=$T/tmp-lane-${TAG}r MAKEFLAGS="-j8 --no-print-directory" TSN_GEN_ROOT=$HOME/milan-fpga-management/tools/tsn-gen-deca300c
mkdir -p "$TMPDIR"
run() { id=$1; shift; { echo "# head $H gate $id: $*"; /usr/bin/time -f "# wall=%e s maxrss=%M kB" bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$(date +%T) $id rc=$rc" >> "$G/summary.txt"; }
echo "$(date +%T) start $H" >> "$G/summary.txt"
run test_builder "python3 sw/builder/test_builder.py --require-rv32"
run behave "cd tests && $SCRATCH/gates/venv/bin/behave --no-capture -f plain"
# a receipt, not a gate: the 32x32 point owes every save group to #823 and exits 1 building nothing
run receipt_target_32x32 "python3 -B tb/verilator/nvm_split_target/run.py --point 32x32 --build-dir $TMPDIR/nvm-target-32x32"
git status --short --untracked-files=all > "$G/tree-after.txt"
echo "$(date +%T) done" >> "$G/summary.txt"
