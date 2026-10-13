#!/usr/bin/env bash
# Scratch: firmware-boundary's gate step, as rtl-fast.yml runs it, timed.
# usage: boundaryjob.sh <tree> <log>
set -u
tree=$1; log=$2
cd "$tree" || exit 2
start=$SECONDS
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator > "$log" 2>&1
rc=$?
echo "rc=$rc $((SECONDS - start)) s" >> "$log"
