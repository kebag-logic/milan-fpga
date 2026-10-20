#!/bin/bash
# Full suite sweep, one shard per call: sweep.sh <outdir> <INDEX/TOTAL>
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator
export VERILATOR_JOBS=2
export TMPDIR=<scratch>/tmp
mkdir -p "$TMPDIR" "$1"
cd <lane>
echo "head $(git rev-parse HEAD) shard $2" > "$1/HEAD.txt"
date -Is > "$1/START.txt"
scripts/run_all_suites.sh "$1" --shard "$2" "${@:3}"
echo "rc=$?" > "$1/RC.txt"
date -Is > "$1/END.txt"
