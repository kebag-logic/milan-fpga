#!/bin/bash
# The CPU budget harness at both points, from a clone, one after another; its misses are its measurement.
# usage: s2harness.sh CLONE BUILD_ROOT LOG_DIR
set -u
S=$MANAGEMENT/2026-09-23/665s3-a697/scripts
C=$1 B=$2 L=$3
mkdir -p "$L"
for p in 1x1 8x8; do
  bash $S/gate.sh "$C" "$L/s2_harness-$p.log" . python3 -B tb/verilator/ctrl_service_budget/run.py --point $p \
    --build-dir "$B/budget-$p" --record-budget-findings --jobs 4
done
