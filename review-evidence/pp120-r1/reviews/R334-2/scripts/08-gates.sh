#!/usr/bin/env bash
# Focused donor gates at head from the scratch export (pinned tool on PATH):
#  1. the PR's own command-decode mutation campaign (tb/pp_top/name_wr_mutant.py)
#  2. zero-tolerance HDL lint (scripts/lint_hdl.sh)
#  3. documentation/inventory gates that need no extra tooling, plus `make stale`
#     and `git diff --check` read-only in the review clone (they need history)
set -uo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); C=${CLONE:-$REVIEWS/r334-2-pp120}; export PATH=$PK/tools:$PATH
export TMPDIR=$PK/scratch/tmp; mkdir -p $TMPDIR
rm -rf $PK/receipts/08-shipped-mutation
python3 $PK/scratch/head/tb/pp_top/name_wr_mutant.py --output $PK/receipts/08-shipped-mutation > $PK/receipts/08-shipped-mutant.log 2>&1
echo "[$?] name_wr_mutant.py campaign"; tail -3 $PK/receipts/08-shipped-mutant.log
cd $PK/scratch/head && ./scripts/lint_hdl.sh > $PK/receipts/08-head-lint.log 2>&1; rc=$?
echo "[$rc] lint_hdl.sh: LINT OK=$(grep -c '^LINT OK' $PK/receipts/08-head-lint.log) FAIL/ERROR=$(grep -c -E '^LINT (FAIL|ERROR)' $PK/receipts/08-head-lint.log)"
for c in "python3 scripts/check-links.py" "python3 scripts/check-matrix.py" \
         "python3 scripts/gen_matrix.py --check" "python3 scripts/check-integrator-params.py" \
         "python3 scripts/check_upc_map.py"; do
  out=$($c 2>&1); rc=$?; echo "[$rc] $c :: $(echo "$out" | tail -1)"
done
out=$(make -s -C $C stale 2>&1); rc=$?; echo "[$rc] make stale (clone) :: ${out:-no stale export}"
git -C $C diff --check a9b7874d415d935949becd7ccfd58799927efb08 83c84b19e09d397ed2eb6f5ace337686ce0ef86b; echo "[$?] git diff --check r2..head"
git -C $C diff --check 0922e43408f891fc0b84a84691df86b4fd0f1c0d 83c84b19e09d397ed2eb6f5ace337686ce0ef86b; echo "[$?] git diff --check base..head"
