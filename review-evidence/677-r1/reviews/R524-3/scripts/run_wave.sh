#!/usr/bin/env bash
# R524-3: run a wave of gates concurrently and wait for all of them in this call.
# Usage: run_wave.sh <clone> <packet> <rv32-gcc> <name>=<command> ...
# Each gate writes receipts/gate-<name>.log and receipts/gate-<name>.rc
# (rc 124 = stopped by the 585 s wave limit, never a pass).
set -u
CLONE=$1 PACKET=$2 CC=$3; shift 3
R=$PACKET/receipts
export MILAN_RV32_CC=$CC TMPDIR=$PACKET/scratch/tmp PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
mkdir -p "$TMPDIR"
cd "$CLONE" || exit 2
for spec in "$@"; do
  name=${spec%%=*} cmd=${spec#*=}
  ( start=$(date +%s); timeout 585 bash -c "$cmd" > "$R/gate-$name.log" 2>&1; rc=$?
    echo $rc > "$R/gate-$name.rc"; echo "$name rc=$rc seconds=$(( $(date +%s) - start ))" ) &
done
wait
