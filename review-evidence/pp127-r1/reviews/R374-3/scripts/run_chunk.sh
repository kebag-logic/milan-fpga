#!/usr/bin/env bash
# Usage: run_chunk.sh <processor-tree> <out-dir> <jobs> <arm,arm,...|ALL>
# Runs the committed tb/srp_top/mutants.py (the recipe of `make -C tb/srp_top mutants`)
# with the pinned simulator first on PATH and scratch-local temp files.
set -u
here=$(cd "$(dirname "$0")" && pwd)
tree=$1; out=$2; jobs=$3; arms=$4
mkdir -p "$out" "$here/../scratch/tmp"
export PATH="$here:$PATH" VJOBS=$jobs TMPDIR="$here/../scratch/tmp"
export REAL_VERILATOR=${REAL_VERILATOR:-$VALIDATION_STORAGE/pp127-manager-0404675d/pinned-tool-bin/verilator}
start=$(date +%s)
if [ "$arms" = ALL ]; then
  make -C "$tree/tb/srp_top" mutants MUTANT_OUTPUT="$out" > "$out/driver.log" 2>&1
else
  python3 "$tree/tb/srp_top/mutants.py" --output "$out" --only "$arms" > "$out/driver.log" 2>&1
fi
echo "DRIVER_RC=$? ELAPSED_S=$(( $(date +%s) - start ))" >> "$out/driver.log"
