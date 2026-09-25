#!/usr/bin/env bash
# Composition static gates for #443 on the merge-train candidate.
# Usage: run_static_gates.sh <clone> <receipts-dir> [python-with-markdown-deps]
set -u
CLONE=${1:?clone}
OUT=${2:?receipts dir}
PY=${3:-python3}
PARENT=ec9cf454bf997fab230d0216dc609e737bc47caa
mkdir -p "$OUT"
cd "$CLONE" || exit 2
run() {
  local name=$1; shift
  "$@" >"$OUT/$name.log" 2>&1
  local rc=$?
  printf '%-40s rc=%d  %s\n' "$name" "$rc" "$*" | tee -a "$OUT/SUMMARY.txt"
}
: >"$OUT/SUMMARY.txt"
echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})" >>"$OUT/SUMMARY.txt"
run docs_check_git            "$PY" scripts/docs_check.py
run docs_check_walk           env GIT_DIR=/dev/null "$PY" scripts/docs_check.py
run gen_toc_check             "$PY" scripts/gen_toc.py --check
run gen_toc_verify_anchors    "$PY" scripts/gen_toc.py --verify-anchors
run docs_check_selftest       "$PY" scripts/docs_check.py --selftest
run check_em_dash_parent      "$PY" scripts/check_em_dash.py --base "$PARENT"
run check_doc_style           "$PY" scripts/check_doc_style.py
run check_doc_paths           "$PY" scripts/check_doc_paths.py
run measure_test_evidence     "$PY" scripts/measure_test_evidence.py --check
run measure_test_evidence_st  "$PY" scripts/measure_test_evidence.py --selftest
run ci_events_check           "$PY" scripts/ci_events.py --check
run ci_events_selftest        "$PY" scripts/ci_events.py --selftest
run check_rtl_source_lists    "$PY" scripts/check_rtl_source_lists.py
run check_sv_idiom            "$PY" scripts/check_sv_idiom.py
run check_cpp_idiom           "$PY" scripts/check_cpp_idiom.py
run check_py_idiom            "$PY" scripts/check_py_idiom.py
run check_feature_status      "$PY" scripts/check_feature_status.py
run check_hygiene             "$PY" scripts/check_hygiene.py --check
run diff_check_parent         git diff --check "$PARENT" HEAD
