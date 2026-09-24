#!/usr/bin/env bash
# Build and run the obj_crflic leg of tb/verilator/milan_dp with a given
# simulator, 8 compile jobs, into a named object directory; print the tally.
# usage: run_crflic.sh <repo> <verilator> <mdir> [extra make args...]
set -uo pipefail
repo=$1; ver=$2; mdir=$3; shift 3
cd "$repo/tb/verilator/milan_dp" || exit 2
start=$(date +%s)
make -s crflic VERILATOR="$ver" VERILATOR_JOBS=8 CRFLIC_MDIR="$mdir" "$@"
rc=$?
echo "make crflic rc=$rc wall_s=$(( $(date +%s) - start ))"
exit $rc
