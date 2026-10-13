#!/usr/bin/env bash
# Scratch: the firmware-boundary command (without its self-test) in a tree whose known set lost a builder, timed.
# usage: probe_drop.sh <tree> <log>
set -u
cd "$1" || exit 2
start=$SECONDS
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator > "$2" 2>&1
echo "rc=$? $((SECONDS - start)) s" >> "$2"
