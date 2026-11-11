#!/usr/bin/env bash
# Build and run milan_dp legs in a given checkout, one log and rc file per leg.
# usage: run_legs.sh <repo-root> <log-dir> <verilator> <jobs> <leg>...
set -u
repo=$1 logs=$2 vl=$3 jobs=$4; shift 4
mkdir -p "$logs"
for leg in "$@"; do
  /usr/bin/time -v make -C "$repo/tb/verilator/milan_dp" VERILATOR="$vl" VERILATOR_JOBS="$jobs" "$leg" \
    > "$logs/$leg.log" 2>&1
  echo $? > "$logs/$leg.rc"
done
echo done > "$logs/ALL.done"
