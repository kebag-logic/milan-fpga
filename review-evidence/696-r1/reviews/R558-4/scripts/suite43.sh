#!/bin/sh
# Usage: suite43.sh <clone> <make-binary-dir> <outdir> <verilator-jobs>
# The full maap suite (`make` = run + mutants) under the given GNU make, invoked
# the hosted way (make -C <suite>) with inherited MAKEFLAGS=w.
set -u
C=$1; MB=$2; OUT=$3; J=$4
export PATH="$MB:$PATH" VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator VERILATOR_JOBS=$J
echo "head=$(git -C "$C" rev-parse HEAD) make=$(make --version | head -1) verilator=$($VERILATOR --version)"
(cd / && env MAKEFLAGS=w make -C "$C/tb/verilator/maap") > "$OUT/suite43.log" 2>&1
echo "suite rc=$?"
grep -E ' checks: | failures|ESCAPED|non-files|Entering directory' "$OUT/suite43.log" | tail -8
