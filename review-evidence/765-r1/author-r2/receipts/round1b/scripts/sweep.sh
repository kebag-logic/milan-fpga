#!/bin/bash
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator
export VERILATOR_JOBS=2
export TMPDIR=<scratch>/tmp
mkdir -p "$TMPDIR"
cd <lane>
echo "head $(git rev-parse HEAD)" > "$1/HEAD.txt"
scripts/run_all_suites.sh "$1"
echo "rc=$?" > "$1/RC.txt"
