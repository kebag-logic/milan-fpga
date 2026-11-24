#!/bin/sh
# Run one milan_dp CI piece through scripts/ci_make_cases.py in a clone,
# recording its transcript, receipt, wall time and exit status.
#   piece_run.sh CLONE SHARD OUTDIR LABEL
set -u
clone=$1 shard=$2 out=$3 label=$4
mkdir -p "$out"
export VERILATOR_JOBS=2 SIM_JOBS=2 MAKEFLAGS='-j1 --no-print-directory' OBJCACHE=
start=$(date +%s)
( cd "$clone" && python3 scripts/ci_make_cases.py --suite milan_dp --shard "$shard" --jobs 2 \
    --receipt "$out/$label.receipt.json" ) > "$out/$label.log" 2>&1
echo "rc=$? wall=$(( $(date +%s) - start ))" > "$out/$label.rc"
