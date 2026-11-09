#!/bin/sh
# usage: run_suite.sh <tree> <receipts-dir> <label> <make-target-or-'mutant'> [jobs]
set -u
T=$1; R=$2; L=$3; W=$4; J=${5:-3}; mkdir -p "$R"
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export TMPDIR=$REVIEWS/854-r804-1-packet/scratch/tmp; mkdir -p "$TMPDIR"
cd "$T/tb/verilator/pp_shadow" || exit 2
"$VERILATOR" --version > "$R/$L.verilator"
if [ "$W" = mutant ]; then
  VERILATOR_JOBS=$J python3 drops_mutant.py > "$R/$L.log" 2>&1; echo $? > "$R/$L.rc"
else
  make --no-print-directory VERILATOR="$VERILATOR" VERILATOR_JOBS=$J $W > "$R/$L.log" 2>&1; echo $? > "$R/$L.rc"
fi
