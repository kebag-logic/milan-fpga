#!/bin/bash
# Run one parent Verilator suite's `run` target on a disposable copy of the
# parent tree whose gptp-processor directory holds the donor tree at REV.
# Usage: parent_suite.sh <label> <donor-rev> <suite-dir-under-tb/verilator>
set -euo pipefail
. "$(dirname "$0")/env.sh"
label=$1; rev=$2; suite=$3
src=$PACKET/scratch/parent
dst=$PACKET/scratch/parent-$label
rm -rf "$dst"; mkdir -p "$dst"
git -C "$src" archive "$PARENT_SHA" | tar -x -C "$dst"
mkdir -p "$dst/third_party/verilog-axis/rtl" "$dst/gptp-processor"
cp "$src/third_party/verilog-axis/rtl/axis_fifo.v" "$dst/third_party/verilog-axis/rtl/"
git -C "$CLONE" archive "$rev" | tar -x -C "$dst/gptp-processor"
echo "verilator: $(command -v verilator) $(verilator --version)"
echo "parent $PARENT_SHA donor $(git -C "$CLONE" rev-parse "$rev") suite $suite label $label"
make -C "$dst/tb/verilator/$suite" run
