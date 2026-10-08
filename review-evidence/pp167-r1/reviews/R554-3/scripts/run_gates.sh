#!/usr/bin/env bash
# R554-3 gates: make check in the review clone, tb/aecp_notify suite in a git-archive copy.
# usage: run_gates.sh <clone> <packet>
set -u
C=$1; P=$2; V=${VERILATOR:?set VERILATOR to the pinned Verilator 5.050 wrapper}
R=$P/receipts; S=$P/scratch/head
rm -rf "$S"; mkdir -p "$S"
git -C "$C" archive bcbf382e5f4d17ccfd8ae75a80bbc45902c75b7d | tar -x -C "$S"
"$V" --version > "$R/verilator_version.txt" 2>&1
( cd "$C" && make check > "$R/make_check.log" 2>&1; echo $? > "$R/make_check.rc" ) &
( cd "$S/tb/aecp_notify" && make VERILATOR="$V" check > "$R/aecp_notify_check.log" 2>&1; echo $? > "$R/aecp_notify_check.rc" ) &
wait
