#!/usr/bin/env bash
# R624-11 composition probes, reproducible from public inputs.
# usage: reproduce.sh <candidate clone at ada26e56> <source clone at f1b2489f> <packet author-r10 dir> <pinned-parser python> <out dir>
#   <packet author-r10 dir>: review-evidence/629-b16-r1/author-r10 at 5775cfa78dc9250ea1b689fc2cfa8e20c41281bb
#   <pinned-parser python>: an interpreter with tools/markdown/requirements.txt installed by hash
set -u
CAND=$1 SRC=$2 E=$3 PY=$4 O=$5
HERE=$(cd "$(dirname "$0")" && pwd)
F=docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md
mkdir -p "$O"
C=$E/tools/check_b16_figures.py
sha256sum "$C"
# 1. the published check, unchanged, on the source head (control) and on the candidate
for t in src cand; do
  D=$SRC; [ $t = cand ] && D=$CAND
  "$PY" -I "$C" "$D/$F" "$E" "$O/$t-rows.tsv" "$O/$t-coverage.tsv" --repo "$D" >"$O/$t.stdout" 2>"$O/$t.stderr"
  echo "$t rc=$?"; head -c 400 "$O/$t.stdout"; echo
done
# 2. probe: the same check with every findings-page row moved by +7 (the #726 note's height), on the candidate
python3 -I "$HERE/shift_rows.py" "$C" "$O/check_shift7.py" 7
"$PY" -I "$O/check_shift7.py" "$CAND/$F" "$E" "$O/cand-shift7-rows.tsv" "$O/cand-shift7-coverage.tsv" --repo "$CAND" \
  >"$O/cand-shift7.stdout" 2>"$O/cand-shift7.stderr"
echo "cand-shift7 rc=$?"
for k in rows coverage; do
  python3 -I "$HERE/norm_lines.py" $k "$O/cand-shift7-$k.tsv" -7 | head -c -1 | cmp - "$O/src-$k.tsv" && echo "$k equal after -7"
done
cmp "$O/cand-shift7.stdout" "$O/src.stdout" && echo "stdout equal"
# 3. every link target of the merged pages
"$PY" -I "$HERE/check_page_links.py" "$CAND" "$F" docs/findings/README.md docs/testing/726_STREAM_COUNTERS.md
