#!/usr/bin/env bash
# Run the static gates that read the files this PR and its predecessors both
# changed, on the candidate tree, one receipt per gate plus a summary line.
# Usage: run_gates.sh <candidate-clone> <receipt-dir> [python-with-markdown-lock]
set -u
REPO=$1; OUT=$2; PY=${3:-python3}
mkdir -p "$OUT"
cd "$REPO" || exit 2
SUM="$OUT/summary.tsv"; : > "$SUM"
run() {
  local name=$1; shift
  "$@" > "$OUT/$name.log" 2>&1; local rc=$?
  printf '%s\t%s\t%s\n' "$name" "$rc" "$*" >> "$SUM"
}
FP=$(git rev-parse HEAD^1)
run docs_check            "$PY" scripts/docs_check.py
run docs_check_selftest   "$PY" scripts/docs_check.py --selftest
run gen_toc_check         "$PY" scripts/gen_toc.py --check
run gen_toc_anchors       "$PY" scripts/gen_toc.py --verify-anchors
run gen_toc_selftest      "$PY" scripts/gen_toc.py --selftest
run em_dash_first_parent  "$PY" scripts/check_em_dash.py --base "$FP"
run em_dash_source_base   "$PY" scripts/check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d
run em_dash_selftest      "$PY" scripts/check_em_dash.py --selftest
run ci_events_check       "$PY" scripts/ci_events.py --check
run ci_events_selftest    "$PY" scripts/ci_events.py --selftest
run ci_scope_selftest     "$PY" scripts/ci_scope.py --selftest
run measure_evidence_check    "$PY" scripts/measure_test_evidence.py --check
run measure_evidence_selftest "$PY" scripts/measure_test_evidence.py --selftest
run suite_shards_selftest "$PY" scripts/suite_shards.py --selftest
run doc_style             "$PY" scripts/check_doc_style.py
run doc_paths             "$PY" scripts/check_doc_paths.py
run py_idiom              "$PY" scripts/check_py_idiom.py
run feature_status        "$PY" scripts/check_feature_status.py
run baremetal_only_check  "$PY" scripts/check_baremetal_only.py --check
run baremetal_only_selftest "$PY" scripts/check_baremetal_only.py --selftest
run gptp_docs             "$PY" scripts/check_gptp_docs.py
run module_matrix_check   "$PY" docs/traceability/gen_module_matrix.py --check
run rtl_source_lists      "$PY" scripts/check_rtl_source_lists.py
run diff_check_parent     git diff --check "$FP" HEAD
run diff_check_source_base git diff --check 57456af96b3127b9d309a995bbbd35a6113ce52d HEAD
cat "$SUM"
