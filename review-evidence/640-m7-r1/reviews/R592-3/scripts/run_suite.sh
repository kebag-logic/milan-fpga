#!/bin/sh
# Run one suite target in the review clone, with its own log and rc file.
# usage: run_suite.sh <clone> <suite-dir> <name> <jobs> <receipts-dir> <tmpdir> [make args...]
set -u
clone=$1; suite=$2; name=$3; jobs=$4; out=$5; tmp=$6; shift 6
V=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
cd "$clone/tb/verilator/$suite" || exit 2
start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
env TMPDIR="$tmp" VERILATOR="$V" VERILATOR_JOBS="$jobs" make "$@" >"$out/$name.log" 2>&1
rc=$?
echo "$rc" >"$out/$name.rc"
echo "start=$start end=$(date -u +%Y-%m-%dT%H:%M:%SZ) rc=$rc suite=$suite args=$*" >"$out/$name.meta"
