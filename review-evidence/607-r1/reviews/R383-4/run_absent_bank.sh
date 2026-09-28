#!/usr/bin/env bash
# Usage: run_absent_bank.sh <clone> <packet>
set -u
CLONE=$1; PKT=$2
export PATH="$PKT/scratch/bin:$PATH"
PY="$HOME/litex-milan/venv/bin/python3"
cd "$CLONE"
start=$(date +%s)
"$PY" -B "$PKT/run_builder_absent.py" "$CLONE" > "$PKT/receipts/13_absent_bank.log" 2>&1
rc=$?
echo "rc=$rc seconds=$(( $(date +%s) - start )) head=$(git rev-parse HEAD)" > "$PKT/receipts/13_absent_bank.rc"
