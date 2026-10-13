#!/usr/bin/env bash
# Scratch: the firmware-unit job's boundary step in one tree against one capture, timed (inside the CI-parity image).
# usage: hgate7.sh <tree> <capture> <log>
set -u
tree=$1; cap=$2; log=$3
cd "$tree" || exit 2
start=$SECONDS
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --capture "$cap" --without verilator > "$log" 2>&1
rc=$?
echo "rc=$rc $((SECONDS - start)) s" >> "$log"
