#!/usr/bin/env bash
# Repository documentation gates that the PR touches (links, matrix, generated matrix, staleness).
source "$(dirname "$0")/00_env.sh"
cd "$TREE"
for c in "python3 scripts/check-links.py" "python3 scripts/check-matrix.py" "python3 scripts/gen_matrix.py --check" "make stale" "git -C $SRC diff --check 008edbbf486598ae237414273d75e385cf0e1a56 $HEAD_SHA"; do
  set +e; out=$($c 2>&1); rc=$?; set -e; echo "== $c rc=$rc"; tail -3 <<<"$out"
done
