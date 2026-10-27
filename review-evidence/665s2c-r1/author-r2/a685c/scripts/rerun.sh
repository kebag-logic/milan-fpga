#!/bin/bash
# One documented harness command, rerun at the lane's checkout to compare its figure with the page.
# usage: rerun.sh CHECKOUT BUILD_DIR LOG -- run.py args...
# The log ends with the elapsed time and the run's rc.
set -u
C=$1 B=$2 L=$3; shift 4
. "$(dirname "$0")/env.sh"
start=$(date +%s)
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --build-dir "$B" "$@" > "$L" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$L"
echo "rc=$rc" >> "$L"
