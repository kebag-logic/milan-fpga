#!/usr/bin/env bash
# Run the explicit crflic-mutants campaign with a given simulator (8 jobs).
# usage: run_crflic_mutants.sh <repo> <verilator>
set -uo pipefail
repo=$1; export VERILATOR=$2; export VERILATOR_JOBS=8
cd "$repo/tb/verilator/milan_dp" || exit 2
start=$(date +%s)
make -s crflic-mutants
rc=$?
echo "make crflic-mutants rc=$rc wall_s=$(( $(date +%s) - start ))"
exit $rc
