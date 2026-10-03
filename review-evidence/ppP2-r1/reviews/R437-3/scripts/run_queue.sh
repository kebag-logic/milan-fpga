#!/usr/bin/env bash
# Run probe specs one after another, each with its own output directory and rc file.
# usage: run_queue.sh REPO PKT VERILATOR JOBS SPEC...
set -u
REPO=$1; PKT=$2; V=$3; J=$4; shift 4
for s in "$@"; do
  n=$(basename "$s" .py)
  python3 "$PKT/scripts/probe.py" --repo "$REPO" --scratch "$PKT/scratch/$n" --out "$PKT/receipts/$n" \
      --jobs "$J" --verilator "$V" --run-timeout 1800 "$s" > "$PKT/scratch/q_$n.out" 2>&1
  echo $? > "$PKT/receipts/$n.rc"
done
