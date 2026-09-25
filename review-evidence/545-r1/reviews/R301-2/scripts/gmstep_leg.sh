#!/usr/bin/env bash
# Connected milan_dp gmstep leg at the head (scratch copy), then the #545
# connection controls (gmstep_mutants.py --slew).
set -u
PKT=${PKT:-$REVIEWS/545-r301-2-packet}
export VERILATOR=${VERILATOR:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator}
export PATH="$(dirname "$VERILATOR"):$PATH"
CPUS=${CPUS:-13,14,15}
cd "$PKT/scratch/tree/tb/verilator/milan_dp" || exit 2
verilator --version
s=$(date +%s)
taskset -c "$CPUS" make gmstep VERILATOR="$VERILATOR"; rc1=$?
echo "GMSTEP_LEG rc=$rc1 wall_s=$(( $(date +%s) - s ))"
s=$(date +%s)
taskset -c "$CPUS" python3 gmstep_mutants.py --slew; rc2=$?
echo "GMSTEP_SLEW_CONTROLS rc=$rc2 wall_s=$(( $(date +%s) - s ))"
[ $rc1 -eq 0 ] && [ $rc2 -eq 0 ]
