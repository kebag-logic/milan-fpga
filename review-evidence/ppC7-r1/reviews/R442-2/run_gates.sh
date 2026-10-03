#!/bin/sh
# Launch the round-2 focused gates concurrently, each with its own log and rc file.
# Usage: run_gates.sh <scratch-dir> <receipts-dir>
# <scratch-dir> holds three clones at the exact head: camp, suite, docs.
S=$1; R=$2
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export TMPDIR=$S/tmp
mkdir -p "$R" "$TMPDIR"
run() { name=$1; shift; ( start=$(date +%s); "$@" > "$R/$name.log" 2>&1; rc=$?; end=$(date +%s); echo "rc=$rc wall_s=$((end-start))" > "$R/$name.rc" ) & }
run ctr_jobs8 python3 "$S/camp/tb/pp_top/ctr_mutants.py" --output "$S/out-j8" --jobs 8
run ctr_jobs1 python3 "$S/camp/tb/pp_top/ctr_mutants.py" --output "$S/out-j1" --jobs 1
run pp_top_suite make -C "$S/suite/tb/pp_top" run
run docs_check make -C "$S/docs" check
wait
