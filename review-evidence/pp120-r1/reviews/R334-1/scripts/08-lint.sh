#!/usr/bin/env bash
# Zero-tolerance HDL lint gate (scripts/lint_hdl.sh) at head with the pinned tool.
set -uo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); export PATH=$PK/tools:$PATH
cd $PK/scratch/head && ./scripts/lint_hdl.sh > $PK/receipts/08-head-lint.log 2>&1; rc=$?
echo "lint_hdl rc=$rc; OK=$(grep -c '^LINT OK' $PK/receipts/08-head-lint.log) FAIL=$(grep -c -E '^LINT (FAIL|ERROR)' $PK/receipts/08-head-lint.log)"
