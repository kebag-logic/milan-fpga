#!/usr/bin/env bash
# Documentation / inventory gates that need no extra tooling, at head.
set -uo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); CLONE=${CLONE:-$REVIEWS/r334-1-pp120}
cd $PK/scratch/head
for c in "python3 scripts/check-links.py" "python3 scripts/check-matrix.py" \
         "python3 scripts/gen_matrix.py --check" "python3 scripts/check-integrator-params.py" \
         "python3 scripts/check_upc_map.py"; do
  out=$($c 2>&1); rc=$?; echo "[$rc] $c :: $(echo "$out" | tail -1)"
done
# staleness needs history: run read-only in the review clone
out=$(make -s -C $CLONE stale 2>&1); rc=$?; echo "[$rc] make stale (clone) :: ${out:-no stale export}"
git -C $CLONE diff --check 0922e43408f891fc0b84a84691df86b4fd0f1c0d a9b7874d415d935949becd7ccfd58799927efb08; echo "[$?] git diff --check base..head"
