#!/bin/bash
# Reviewer rerun of one harness arm at the checkout's head.
# usage: rerun.sh CHECKOUT BUILD_DIR LOG RC -- run.py args...
set -u
C=$1 B=$2 L=$3 R=$4; shift 5
. "$(dirname "$0")/../env.sh"
start=$(date +%s)
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --build-dir "$B" "$@" > "$L" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$L"
echo "$rc" > "$R"
