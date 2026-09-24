#!/usr/bin/env bash
# [R293] R293-3: containment self-test parity, PR source head vs candidate.
# Usage: selftest_parity.sh <repo> <python> <scratch-dir> <outdir>
# Extracts each commit's tree with git archive (no worktree, no checkout),
# runs `check_merge_containment.py --selftest` there, and diffs the case lines.
set -u
REPO=$1 PY=$2 SCR=$3 OUT=$4
mkdir -p "$OUT"
for c in b0347a4fd668f8d40bdf40a142ac0ea70167acd1 177867daf3b35ba41b8c51f8c35c8509643dda22; do
  d="$SCR/parity-$c"; rm -rf "$d"; mkdir -p "$d"
  git -C "$REPO" archive "$c" scripts | tar -x -C "$d"
  # The checker needs a repository with at least one commit.
  git -C "$d" init -q && git -C "$d" add -A &&
    git -C "$d" -c user.name=r293 -c user.email=r293@invalid -c commit.gpgsign=false \
      commit -q -m "extracted $c scripts"
  (cd "$d" && "$PY" scripts/check_merge_containment.py --selftest) > "$OUT/selftest-$c.log" 2>&1
  echo "$c rc=$?"
  grep -E '^  (ok|FAIL|NOT RUN) ' "$OUT/selftest-$c.log" > "$OUT/cases-$c.txt"
  echo "$c cases=$(wc -l < "$OUT/cases-$c.txt") ok=$(grep -c '^  ok ' "$OUT/cases-$c.txt")"
done
if cmp -s "$OUT/cases-b0347a4fd668f8d40bdf40a142ac0ea70167acd1.txt" \
          "$OUT/cases-177867daf3b35ba41b8c51f8c35c8509643dda22.txt"; then
  echo "PARITY: identical case lines"; else echo "PARITY: case lines DIFFER"; fi
