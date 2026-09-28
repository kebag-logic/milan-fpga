#!/usr/bin/env bash
# Full builder bank on the candidate, bench LiteX interpreter, pinned sv2v/Verilator first on PATH.
# Usage: run_bench_bank.sh <clone> <packet>
set -u
CLONE=$1; PKT=$2
export PATH="$PKT/scratch/bin:$PATH"
export MILAN_LITEX_PYTHON="$HOME/litex-milan/venv/bin/python3"
cd "$CLONE"
start=$(date +%s)
"$MILAN_LITEX_PYTHON" -B sw/builder/test_builder.py --require-rv32 --require-elaboration > "$PKT/receipts/10_bench_bank.log" 2>&1
rc=$?
echo "rc=$rc seconds=$(( $(date +%s) - start )) head=$(git rev-parse HEAD)" > "$PKT/receipts/10_bench_bank.rc"
