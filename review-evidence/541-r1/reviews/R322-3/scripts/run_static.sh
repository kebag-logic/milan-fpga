#!/bin/bash
# Run the static gates that read the composed overlap files (and the PR's
# own files) on the candidate clone. Usage: run_static.sh <clone> <outdir> <python>
# Each gate runs in the foreground; its output goes to <outdir>/<n>.log and
# its exit status to <outdir>/summary.tsv.
set -u
CLONE=$1; OUT=$2; PY=$3; PARENT=${PARENT:-b1b334725dcf12e084eaa3bb96b1e6865c052267}
mkdir -p "$OUT"; cd "$CLONE" || exit 2
: > "$OUT/summary.tsv"
n=0
run() {
  n=$((n+1)); local log; log=$(printf '%s/%02d.log' "$OUT" "$n")
  { echo "\$ $*"; "$@"; } > "$log" 2>&1; local rc=$?
  printf '%02d\t%s\t%s\n' "$n" "$rc" "$*" >> "$OUT/summary.tsv"
}
run $PY scripts/measure_test_evidence.py --check
run $PY scripts/measure_test_evidence.py --selftest
run $PY scripts/docs_check.py
run $PY scripts/gen_toc.py --selftest
run $PY scripts/gen_toc.py --verify-anchors
run $PY scripts/gen_toc.py --check
run $PY scripts/check_em_dash.py --base "$PARENT"
run $PY scripts/check_doc_style.py
run $PY scripts/check_doc_style.py --selftest
run $PY scripts/check_doc_paths.py
run $PY docs/traceability/gen_module_matrix.py --check
run $PY docs/DOC_MAP.gen.py --check
run $PY scripts/check_solution_docs.py
run $PY scripts/check_feature_status.py
run $PY scripts/check_feature_status.py --self-test
run $PY scripts/check_hygiene.py --check
run $PY scripts/check_sv_idiom.py
run $PY scripts/check_cpp_idiom.py
run $PY scripts/check_py_idiom.py
run $PY scripts/check_todo_ownership.py
run $PY scripts/measure_fail_fast.py --check
run $PY scripts/measure_naming.py --check
run $PY scripts/check_port_contracts.py
run $PY scripts/check_rtl_source_lists.py
run $PY scripts/check_archive.py
run $PY scripts/ci_events.py --check
run $PY scripts/ci_events.py --selftest
run git -c core.pager=cat diff --check "$PARENT" HEAD
run git -c core.pager=cat diff --check a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4 HEAD
