#!/bin/sh
# Usage: run_suite_at.sh <commit> <label>
# Exports hdl/ and tb/{common,adp_engine} of <commit> into scratch and runs tb/adp_engine.
. "$(dirname "$0")/env.sh"
set -u
c=$1; label=$2
d="$SCRATCH/suite-$label"; rm -rf "$d"; mkdir -p "$d"
git -C "$CLONE" archive "$c" hdl tb/common tb/adp_engine | tar -x -C "$d"
"$VERILATOR" --version > "$RCPT/suite-$label.log"
make -C "$d/tb/adp_engine" run VERILATOR="$VERILATOR" >> "$RCPT/suite-$label.log" 2>&1
rc=$?; echo "$rc" > "$RCPT/suite-$label.rc"; exit $rc
