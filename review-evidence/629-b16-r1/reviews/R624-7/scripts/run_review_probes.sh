#!/usr/bin/env bash
# R624-7: run the ten published review probes, unchanged, against the round-7 check and the head page.
# usage: run_review_probes.sh <repo clone at head> <author-r7 packet copy> <renderer python> <work dir> <receipt dir>
set -u
REPO=$1 PKT=$2 RPY=$3 WORK=$4 OUT=$5
PR=$PKT/tools/review-probes
CHK=$PKT/tools/check_b16_figures.py
PAGE=$REPO/docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md
mkdir -p "$WORK" "$OUT"
run() { # name, python, script, args...
  local n=$1 py=$2 s=$3; shift 3
  rm -rf "$WORK/$n"; mkdir -p "$WORK/$n/receipts" "$WORK/$n/scratch"
  "$py" -I "$PR/$s" "$@" > "$OUT/$n.stdout" 2>&1; echo "$?" > "$OUT/$n.rc"
  echo "$n rc=$(cat "$OUT/$n.rc")"
}
P=python3
run r624-4 $P probe_escape_forms.py "$REPO" "$PKT" "$WORK/r624-4/scratch" "$WORK/r624-4/out.json"
run r625-4 $P probe_coverage.py "$REPO" "$PKT" "$WORK/r625-4"
run r625-3 $P probe_figure_coverage.py "$REPO" "$PKT" "$WORK/r625-3"
run r624-5-row3200 $P probe_row3200.py "$REPO" "$PKT" "$WORK/r624-5-row3200/scratch" "$WORK/r624-5-row3200/out.json"
run r624-5-escapes $P probe_r624_5_escapes.py "$REPO" "$PKT" "$WORK/r624-5-escapes/scratch" "$WORK/r624-5-escapes/out.json"
run r625-5-comment $P probe_comment_separator.py "$REPO" "$PKT" "$WORK/r625-5-comment"
run r625-6-rendered "$RPY" probe_rendered_comment.py "$REPO" "$PKT" "$WORK/r625-6-rendered"
run r625-6-followers $P probe_followers.py "$REPO" "$PKT" "$WORK/r625-6-followers"
run r624-6-escapes $P probe_r624_6_escapes.py "$CHK" "$PAGE" "$PKT" "$REPO" "$WORK/r624-6-escapes/scratch" "$WORK/r624-6-escapes/out.json"
run r624-6-row3200-polls $P probe_row3200_polls.py "$CHK" "$PAGE" "$PKT" "$REPO" "$WORK/r624-6-row3200-polls/work" "$WORK/r624-6-row3200-polls/out.json"
