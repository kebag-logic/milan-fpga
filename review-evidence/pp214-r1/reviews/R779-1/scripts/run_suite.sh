#!/bin/bash
# usage: run_suite.sh <tree> <suite> <group-or-empty> <logname>
# Runs one Verilator suite of a disposable tree with the scoped toolchain; rc lands beside the log.
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
export PATH=${VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}:$PATH
t=$1; s=$2; g=$3; l=$4
make -C "$t/tb/$s" ${g:+RUN_ARGS=$g} > "$PKT/scratch/logs/$l.log" 2>&1
echo $? > "$PKT/scratch/logs/$l.rc"
