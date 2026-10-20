#!/bin/bash
# Full suite sweep, one shard per call, in its own clean clone: sweep.sh <clone> <outdir> <INDEX/TOTAL>
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator
export VERILATOR_JOBS=2
export TMPDIR=<scratch>/round1c/tmp
mkdir -p "$TMPDIR" "$2"
cd "$1"
echo "head $(git rev-parse HEAD) shard $3" > "$2/HEAD.txt"
date -Is > "$2/START.txt"
scripts/run_all_suites.sh "$2" --shard "$3"
echo "rc=$?" > "$2/RC.txt"
date -Is > "$2/END.txt"
