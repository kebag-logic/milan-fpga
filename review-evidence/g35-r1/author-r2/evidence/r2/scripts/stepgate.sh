#!/usr/bin/env bash
# Run make docs, make lint and the parser mutation arm concurrently.
# Usage: stepgate.sh <out-dir>
set -u
O="$1"; mkdir -p "$O"
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
export TMPDIR=$VALIDATION_STORAGE/g35-a599/tmp PYTHONDONTWRITEBYTECODE=1
cd $LANES/g35-rx-err || exit 2
(make docs > "$O/docs.log" 2>&1; echo $? > "$O/docs.rc") &
(make lint > "$O/lint.log" 2>&1; echo $? > "$O/lint.rc") &
(cd tb/verilator/parser && python3 mutants.py > "$O/mutants.log" 2>&1; echo $? > "$O/mutants.rc") &
wait
for g in docs lint mutants; do echo "$g rc=$(cat "$O/$g.rc")"; done
