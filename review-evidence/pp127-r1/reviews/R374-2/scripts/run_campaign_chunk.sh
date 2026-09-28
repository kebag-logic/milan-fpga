#!/usr/bin/env bash
# Usage: run_campaign_chunk.sh <processor-tree> <out-dir> <jobs:4|8> <arm,arm,...>
# Runs the committed tb/srp_top/mutants.py driver on a chunk of arms with the
# pinned simulator (compile parallelism capped) and scratch-local temp files.
set -u
here=$(cd "$(dirname "$0")" && pwd)
tree=$1; out=$2; jobs=$3; arms=$4
mkdir -p "$out" "$here/../scratch/tmp"
export VERILATOR="$here/verilator-j$jobs" TMPDIR="$here/../scratch/tmp"
python3 "$tree/tb/srp_top/mutants.py" --output "$out" --only "$arms" > "$out/driver.log" 2>&1
echo "DRIVER_RC=$?" >> "$out/driver.log"
