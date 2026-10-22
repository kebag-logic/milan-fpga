#!/usr/bin/env bash
# sweep.sh OUTDIR [--physical-gptp]: the parent sweep at the committed head,
# from the physical worktree path, with the lane environment; rc files beside.
set -u
out="$1"; shift
mkdir -p "$out"
source $VALIDATION_STORAGE/scratch/a662/env.sh
export MILAN_RV32_CC=$VALIDATION_STORAGE/771-a662-r2/rv32-sdk/host/bin/riscv32-linux-gcc
export TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/a662/tsn-gen
unset MAKEFLAGS
cd $LANES/771-pin4 || exit 2
if [ "${1:-}" = "--physical-gptp" ]; then
    export SUITE_SWEEP_LOCK=$VALIDATION_STORAGE/771-a662-r2/physical.lock
fi
{
    echo "head=$(git rev-parse HEAD)"
    echo "processor=$(git -C protocol-processor rev-parse HEAD)"
    echo "gptp=$(git -C gptp-processor rev-parse HEAD)"
    echo "dirty=$(git status --porcelain | wc -l)"
    make --version | head -n 1
    "$VERILATOR" --version
    echo "VERILATOR_JOBS=$VERILATOR_JOBS PYTHON_CPU_COUNT=$PYTHON_CPU_COUNT TSN_GEN_ROOT=$TSN_GEN_ROOT SUITE_SWEEP_LOCK=${SUITE_SWEEP_LOCK:-default} args=$*"
    date -Is
} > "$out/env.txt"
t0=$SECONDS
bash scripts/run_all_suites.sh "$out/logs" "$@" > "$out/sweep.out" 2>&1
echo $? > "$out/sweep.rc"
echo $((SECONDS - t0)) > "$out/sweep.seconds"
python3 scripts/suite_tally.py --quiet --expect-suite-root tb/verilator "$@" "$out/logs" > "$out/tally.out" 2>&1
echo $? > "$out/tally.rc"
date -Is > "$out/done"
