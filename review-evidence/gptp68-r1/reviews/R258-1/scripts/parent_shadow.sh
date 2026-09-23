#!/bin/bash
# Run the parent's tb/verilator/gptp_shadow `run` target (no mutants) on a
# disposable copy of the parent tree whose gptp-processor directory holds the
# donor tree at REV. Usage: parent_shadow.sh <label> <donor-rev> [patch...]
# Each optional patch is applied to the parent copy (probe instrumentation).
set -euo pipefail
. "$(dirname "$0")/env.sh"
label=$1; rev=$2; shift 2
src=$PACKET/scratch/parent
dst=$PACKET/scratch/parent-$label
rm -rf "$dst"; mkdir -p "$dst"
git -C "$src" archive "$PARENT_SHA" | tar -x -C "$dst"
mkdir -p "$dst/third_party/verilog-axis/rtl" "$dst/gptp-processor"
cp "$src/third_party/verilog-axis/rtl/axis_fifo.v" "$dst/third_party/verilog-axis/rtl/"
git -C "$CLONE" archive "$rev" | tar -x -C "$dst/gptp-processor"
for p in "$@"; do patch -d "$dst" -p1 < "$p"; done
echo "verilator: $(command -v verilator) $(verilator --version)"
echo "parent $PARENT_SHA donor $(git -C "$CLONE" rev-parse "$rev") label $label"
make -C "$dst/tb/verilator/gptp_shadow" run
