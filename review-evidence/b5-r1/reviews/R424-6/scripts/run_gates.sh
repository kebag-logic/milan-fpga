#!/usr/bin/env bash
# Run the documentation gates that read the files this PR and its composed
# predecessor touch, on a clean checkout of the candidate. Usage:
#   run_gates.sh <checkout> <python-with-markdown-lock> <receipt-dir>
set -u
REPO=$1; PY=$2; OUT=$3
mkdir -p "$OUT"
cd "$REPO" || exit 2
DEV=ea3fb38877842f223afea97e3bd72a10500455c9
MB=e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b
run() { name=$1; shift
  "$@" > "$OUT/$name.log" 2>&1; rc=$?
  printf '%-34s rc=%s  %s\n' "$name" "$rc" "$*" | tee -a "$OUT/summary.txt"; }
: > "$OUT/summary.txt"
echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})" >> "$OUT/summary.txt"
run docs_check            "$PY" scripts/docs_check.py
run em_dash_base_dev      "$PY" scripts/check_em_dash.py --base "$DEV"
run em_dash_base_mb       "$PY" scripts/check_em_dash.py --base "$MB"
run em_dash_selftest      "$PY" scripts/check_em_dash.py --selftest
run doc_style             "$PY" scripts/check_doc_style.py
run doc_style_selftest    "$PY" scripts/check_doc_style.py --selftest
run doc_paths             "$PY" scripts/check_doc_paths.py
run doc_map_check         "$PY" docs/DOC_MAP.gen.py --check
run doc_map_selftest      "$PY" docs/DOC_MAP.gen.py --selftest
run solution_docs         "$PY" scripts/check_solution_docs.py
run feature_status        "$PY" scripts/check_feature_status.py
run feature_status_self   "$PY" scripts/check_feature_status.py --self-test
run gen_toc_selftest      "$PY" scripts/gen_toc.py --selftest
run gen_toc_anchors       "$PY" scripts/gen_toc.py --verify-anchors
run gen_toc_check         "$PY" scripts/gen_toc.py --check
run hygiene_check         "$PY" scripts/check_hygiene.py --check
run archive               "$PY" scripts/check_archive.py
run ci_events_check       "$PY" scripts/ci_events.py --check
run ci_events_selftest    "$PY" scripts/ci_events.py --selftest
run module_matrix_check   "$PY" docs/traceability/gen_module_matrix.py --check
run test_evidence_check   "$PY" scripts/measure_test_evidence.py --check
echo "post-status: $(git status --porcelain | wc -l) dirty paths" >> "$OUT/summary.txt"
