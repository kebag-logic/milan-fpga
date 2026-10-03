#!/bin/sh
# Reproduce the R454-2 receipts. Inputs, all public:
#   REPO   a checkout of kebag-logic/milan-fpga at 77299b4fca1ec3268f0997c55a51d84955bbfeca
#   EVGIT  a git dir holding branch 629-b8-review-evidence (commits 5bad6a43, 36ee6d8a, d6cc650f)
#   PY     a python with the pinned Markdown lock (tools/markdown/requirements.txt) and pyyaml
#   OUT    an output directory
set -eu
: "${REPO:?}" "${EVGIT:?}" "${PY:?}" "${OUT:?}"
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT/ev36" "$OUT/evd6" "$OUT/gates"
git -C "$EVGIT" archive 36ee6d8a review-evidence/629-b8-r1 | tar -x -C "$OUT/ev36"
git -C "$EVGIT" archive d6cc650f review-evidence/629-b8-r1/author-r2 | tar -x -C "$OUT/evd6"
PAGE="$REPO/docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
EV="$OUT/ev36/review-evidence/629-b8-r1"
python3 "$HERE/check_b8_rows.py" "$PAGE" "$EV" "$OUT/evd6/review-evidence/629-b8-r1/author-r2/redaction.json" > "$OUT/check-b8-rows.txt"
python3 "$HERE/check_fragments.py" "$REPO" > "$OUT/fragments.txt"
python3 "$HERE/derive_round2_figures.py" "$EV/author" > "$OUT/derive-round2-figures.txt"
python3 "$HERE/privacy_scan.py" "$EVGIT" "$PAGE" "$EV/author" "$OUT/evd6/review-evidence/629-b8-r1/author-r2" > "$OUT/privacy-scan.txt"
cd "$REPO"
for g in "docs_check scripts/docs_check.py" "doc_style scripts/check_doc_style.py" \
         "gen_toc_check scripts/gen_toc.py --check" "gen_toc_anchors scripts/gen_toc.py --verify-anchors" \
         "em_dash scripts/check_em_dash.py --base 40714c1bd166c2a05f9607a861e8550c705d183a" \
         "doc_paths scripts/check_doc_paths.py" "ci_scope_selftest scripts/ci_scope.py --selftest" \
         "baremetal_check scripts/check_baremetal_only.py --check" \
         "baremetal_selftest scripts/check_baremetal_only.py --selftest" \
         "feature_status scripts/check_feature_status.py --self-test"; do
  set -- $g; n=$1; shift
  rc=0; "$PY" "$@" > "$OUT/gates/$n.log" 2>&1 || rc=$?
  echo "$n rc=$rc" >> "$OUT/gates/summary.txt"
done
rc=0; git diff --check 40714c1bd166c2a05f9607a861e8550c705d183a HEAD > "$OUT/gates/diff_check_base.log" 2>&1 || rc=$?
echo "diff_check_base rc=$rc" >> "$OUT/gates/summary.txt"
rc=0; git diff --check 4fb5125a2e43997384839deeb1fe4742a5b2dca8 HEAD > "$OUT/gates/diff_check_r1.log" 2>&1 || rc=$?
echo "diff_check_r1 rc=$rc" >> "$OUT/gates/summary.txt"
