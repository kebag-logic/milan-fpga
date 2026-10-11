#!/usr/bin/env bash
# The builder bank (sw/builder/test_builder.py --require-elaboration
# --require-rv32) in six consecutive parts by its own function list, one after
# another, each logged with its rc and elapsed time. A scratch sitecustomize
# caps os.cpu_count() at four; the pinned Verilator 5.050, GNU make 4.3, the
# RV32 SDK and CPython 3.12.3 come first on PATH.
# Usage: builder_bank.sh <repo> <logdir> <sitecustomize-dir>
set -u
repo=$1; logs=$2; site=$3
here=$(cd "$(dirname "$0")" && pwd)
export PATH="$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_STORAGE/641-a573/make-4.3:$VALIDATION_STORAGE/671-a592/venv312/bin:$HOME/br-milan-rv32/host/bin:$PATH"
export VERILATOR_JOBS=2 TMPDIR=$VALIDATION_STORAGE/671-a592/r6/tmp PYTHONPATH="$site"
cd "$repo" || exit 2
for part in 0 1 2 3 4 5; do
  start=$(date +%s.%N)
  python3 "$here/builder_parts.py" "$repo" "$part" 6 --require-elaboration --require-rv32 > "$logs/part$((part + 1)).log" 2>&1
  rc=$?
  echo "elapsed=$(python3 -c "print(round($(date +%s.%N) - $start, 2))") rc=$rc" >> "$logs/part$((part + 1)).log"
  echo "part $((part + 1)) rc=$rc $(date -Is)"
done
