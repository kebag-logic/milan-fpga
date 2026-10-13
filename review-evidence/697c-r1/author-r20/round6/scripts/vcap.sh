#!/usr/bin/env bash
# Scratch: the three Verilator builders of one tree under one capture, each timed (one at a time).
# usage: vcap.sh <tree> <capture> <work>
set -u
tree=$1; cap=$2; work=$3
export TMPDIR=$VALIDATION_STORAGE/697c-a583/tmpdir VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator VERILATOR_JOBS=2
export MILAN_RV32_CC=$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc
cd "$tree" || exit 2
rm -rf "$cap" "$work"; mkdir -p "$work"
c() { local start=$SECONDS; python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$cap" -- "$@" > "$work/$(basename "$2" .py).log" 2>&1; echo "rc=$? after $((SECONDS - start)) s: $*"; }
c make -C tb/verilator/mbx VERILATOR="$VERILATOR" VBUILD_JOBS=4
c python3 sw/firmware/ctrl/test/maap_differential.py --self-test
c python3 sw/firmware/ctrl/test/aecp_wire.py --reference protocol-processor --interfaces 1 --output "$work/aecp-wire" --verilator "$VERILATOR"
echo DONE
