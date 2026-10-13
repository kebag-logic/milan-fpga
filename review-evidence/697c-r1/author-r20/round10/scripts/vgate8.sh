#!/usr/bin/env bash
# Scratch: firmware-verilator's gate step in one tree, timed (run inside the CI-parity image).
# usage: vgate8.sh <tree> <log>
set -u
tree=$1; log=$2
export VERILATOR_JOBS=2
cd "$tree" || exit 2
git clean -fdxq tb/verilator/mbx
start=$SECONDS
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator > "$log" 2>&1
rc=$?
echo "rc=$rc $((SECONDS - start)) s" >> "$log"
