#!/bin/sh
# run_pair.sh CLONE PACKET: the coverage gate and the ctrl firmware gate, side by side,
# each with its own log and rc under PACKET/receipts/r530.
C=$1; P=$2/receipts/r530
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$P"
cd "$C" || exit 2
( timeout 580 python3 sw/firmware/gtest/fw_coverage.py --check --jobs 2 > "$P/coverage_check.log" 2>&1; echo $? > "$P/coverage_check.rc" ) &
( timeout 580 python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-dir "$2/scratch/posbuild" > "$P/ctrl_gate.log" 2>&1; echo $? > "$P/ctrl_gate.rc" ) &
wait
