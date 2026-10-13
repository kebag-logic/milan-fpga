#!/usr/bin/env bash
# R624-12: figure-check runs on the candidate and source pages, the rebuild, and the reviewer's +7 probe.
# usage: run_checks.sh CANDIDATE_REPO SOURCE_REPO R10_PACKET R11_PACKET PARSER_PY OUT
# Runs the independent jobs concurrently, each with its own log and rc file, then waits on all of them.
set -uo pipefail
CAND=$1 SRC=$2 R10=$3 R11=$4 PY=$5 OUT=$6
HERE=$(cd "$(dirname "$0")" && pwd)
F=docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md
mkdir -p "$OUT"
run() { # tag check page repo
  local tag=$1 chk=$2 page=$3 repo=$4 rc=0
  timeout 300s "$PY" -I -B "$chk" "$page" "$R10" "$OUT/$tag-rows.tsv" "$OUT/$tag-coverage.tsv" --repo "$repo" \
    >"$OUT/$tag.stdout" 2>"$OUT/$tag.stderr" || rc=$?
  echo "$rc" >"$OUT/$tag.rc"
}
# reviewer's own +7 probe of the source check (independent of the author's build)
"$PY" -I -B "$HERE/shift_rows.py" "$R10/tools/check_b16_figures.py" 7 "$OUT/probe-plus7-check.py" \
  "$OUT/probe-plus7-shift.json" >"$OUT/probe-plus7-shift.stdout"
# rebuild from the published spec and build with the candidate page as the only changed input
( timeout 120s "$PY" -I -B "$R11/tools/r10_figures_build.py" "$CAND/$F" "$R11/tools/r10_figures_spec.py" \
    "$R10/tools/check_b16_figures.py" "$OUT/rebuilt-cand-check.py" >"$OUT/rebuild-cand.stdout" 2>&1; echo $? >"$OUT/rebuild-cand.rc" ) &
( timeout 120s "$PY" -I -B "$R10/tools/r10_figures_build.py" "$SRC/$F" "$R10/tools/r10_figures_spec.py" \
    "$R10/tools/check_b16_figures.py" "$OUT/rebuilt-src-check.py" >"$OUT/rebuild-src.stdout" 2>&1; echo $? >"$OUT/rebuild-src.rc" ) &
run cand-r11 "$R11/tools/check_b16_figures.py" "$CAND/$F" "$CAND" &
run cand-r10 "$R10/tools/check_b16_figures.py" "$CAND/$F" "$CAND" &
run src-r10 "$R10/tools/check_b16_figures.py" "$SRC/$F" "$SRC" &
run cand-probe7 "$OUT/probe-plus7-check.py" "$CAND/$F" "$CAND" &
run src-r11 "$R11/tools/check_b16_figures.py" "$SRC/$F" "$SRC" &
wait
for t in rebuild-cand rebuild-src cand-r11 cand-r10 src-r10 cand-probe7 src-r11; do echo "$t rc=$(cat "$OUT/$t.rc")"; done
