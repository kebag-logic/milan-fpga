#!/usr/bin/env bash
# Round 11: R624-11 reproduce.sh step 1, with separate source and candidate checks.
# Usage: reproduce.sh CANDIDATE_INPUT SOURCE_REPO PREVIOUS_PACKET PARSER_PY OUTPUT_DIR
# The input may be a candidate checkout or exact page fixtures; SOURCE_REPO supplies history.
# Run this script under an outer timeout. All work stays in the foreground.
set -euo pipefail
CAND=$1 SRC=$2 PREVIOUS=$3 PY=$4 OUT=$5
HERE=$(cd "$(dirname "$0")" && pwd)
F=docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md
export GIT_DIR
GIT_DIR=$(timeout 15s git -C "$SRC" rev-parse --absolute-git-dir)
timeout 10s mkdir -p "$OUT"
# Step 1: source uses author-r10, cand uses author-r11, unchanged in each run.
for tag in src cand; do
  PAGE="$SRC/$F"; REPO=$SRC; CHECK="$PREVIOUS/tools/check_b16_figures.py"
  if [ "$tag" = cand ]; then
    PAGE="$CAND/$F"; REPO=$CAND; CHECK="$HERE/check_b16_figures.py"
  fi
  rc=0
  timeout 120s "$PY" -I -B "$CHECK" "$PAGE" "$PREVIOUS" \
    "$OUT/$tag-rows.tsv" "$OUT/$tag-coverage.tsv" --repo "$REPO" \
    >"$OUT/$tag.stdout" 2>"$OUT/$tag.stderr" || rc=$?
  printf '%s\n' "$rc" >"$OUT/$tag.rc"
  printf '%s rc=%s\n' "$tag" "$rc"
  test "$rc" -eq 0
  timeout 10s cat "$OUT/$tag.stdout"
done
# Step 2: regeneration from spec/build must be byte-identical.
timeout 30s "$PY" -I -B "$HERE/r10_figures_build.py" "$CAND/$F" \
  "$HERE/r10_figures_spec.py" "$PREVIOUS/tools/check_b16_figures.py" \
  "$OUT/rebuilt-check.py" >"$OUT/build.stdout"
timeout 10s cmp "$HERE/check_b16_figures.py" "$OUT/rebuilt-check.py"
# Step 3: same rows, values and coverage after moving candidate page lines back by seven.
timeout 30s "$PY" -I -B "$HERE/compare_figures.py" "$OUT"
