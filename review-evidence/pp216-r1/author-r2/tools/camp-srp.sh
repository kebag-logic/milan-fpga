#!/usr/bin/env bash
# camp-srp.sh <runs> <clone>: the SRP mutant campaign (the job CI runs as make -C tb/srp_top mutants) with --jobs 8, the
# pinned Verilator with its build parallelism capped first on PATH, TMPDIR on disk
R=$1; C=$2
. "$(dirname "$0")/common.sh"
mkdir -p "$R" "$S/tmp/camp"
export TMPDIR=$S/tmp/camp VL_BUILD_J=2
g "$R" "$C" "$V" "$V/bin:$T/vl-cap:$BASE" camp-srp python3 -B tb/srp_top/mutants.py --output "$R/camp-srp-out" --jobs 8
