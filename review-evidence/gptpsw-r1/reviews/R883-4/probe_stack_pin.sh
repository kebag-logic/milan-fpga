#!/bin/sh
# Reviewer probe: the gPTP simulation's stack-pin prerequisite and STACK_DIR.
# usage: probe_stack_pin.sh <checkout> <scratch-dir>
set -u
R=$1; S=$2; C=$S/stack-copy
rm -rf "$C"; git clone -q --no-hardlinks "$R/third_party/tsn-c-stack" "$C"
git -C "$C" checkout -q "$(git -C "$R" rev-parse HEAD:third_party/tsn-c-stack)"
echo "== 1 pristine copy: stack-pin"; make -s -C "$R/tb/verilator/gptp_sw" stack-pin STACK_DIR="$C"; echo "rc=$?"
echo "== 2 dry-run build names the supplied include dir"
make -n -C "$R/tb/verilator/gptp_sw" build STACK_DIR="$C" MDIR="$S/gsim-dry" | grep -c -- "-I$C/include"
make -n -C "$R/tb/verilator/gptp_sw" build STACK_DIR="$C" MDIR="$S/gsim-dry" | grep -c -- "third_party/tsn-c-stack/include"
echo "== 3 edited header: stack-pin"; printf '/* local */\n' >> "$C/include/adp.h"
make -s -C "$R/tb/verilator/gptp_sw" stack-pin STACK_DIR="$C"; echo "rc=$?"
echo "== 4 edited header: build stops before any compile"
make -C "$R/tb/verilator/gptp_sw" build STACK_DIR="$C" MDIR="$S/gsim-bad" VERILATOR=false CC=false 2>&1 | tail -n 4; echo "objects: $(ls "$S/gsim-bad/fw" 2>/dev/null | wc -l)"
git -C "$C" checkout -q -- include/adp.h
echo "== 5 another revision: stack-pin"; git -C "$C" checkout -q HEAD~1
make -s -C "$R/tb/verilator/gptp_sw" stack-pin STACK_DIR="$C"; echo "rc=$?"
