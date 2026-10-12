#!/usr/bin/env bash
# Scratch (M8a-1 round 5): the LiteX aggregate and its selftest in the litex_pins.txt-only
# CPython 3.12.3 interpreter, pinned Verilator 5.050, a HOME holding only the pinned RV32 SDK.
# usage: litex_aggregate.sh <tree> <logs>
set -u
T=$1
O=$2
mkdir -p "$O/sims"
export HOME=$VALIDATION_STORAGE/640m8a-a594/r3/final/fakehome
export PATH=$VALIDATION_STORAGE/640m8a-a594/r3/ci-venv/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:/usr/local/bin:/usr/bin:/bin
export MILAN_LITEX_PYTHON=$VALIDATION_STORAGE/640m8a-a594/r3/ci-venv/bin/python3
export TMPDIR=$VALIDATION_STORAGE/640m8a-a594/r5/tmp PYTHONDONTWRITEBYTECODE=1 VERILATOR_JOBS=2 MAKEFLAGS=-j8
cd "$T" || exit 9
git rev-parse HEAD > "$O/head.txt"
git status --porcelain > "$O/status-before.txt"
{ command -v python3; python3 --version; verilator --version; } > "$O/env.txt" 2>&1
date -Is > "$O/start.txt"
scripts/run_litex_sims.sh --selftest > "$O/selftest.log" 2>&1
echo $? > "$O/selftest.rc"
scripts/run_litex_sims.sh "$O/sims" > "$O/aggregate.log" 2>&1
echo $? > "$O/aggregate.rc"
git status --porcelain > "$O/status-after.txt"
date -Is > "$O/end.txt"
