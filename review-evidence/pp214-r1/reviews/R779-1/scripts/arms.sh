#!/bin/bash
# Runs the named author arms through the repository's own campaign driver, from a disposable tree.
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
export PATH=${VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}:$PATH
export TMPDIR=$PKT/scratch/tmp; mkdir -p "$TMPDIR"
cd "$PKT/scratch/head" && python3 tb/srp_top/mutants.py --output "$PKT/scratch/arms" --jobs 8 --only "$1" > "$PKT/scratch/logs/arms.log" 2>&1
echo $? > "$PKT/scratch/logs/arms.rc"
