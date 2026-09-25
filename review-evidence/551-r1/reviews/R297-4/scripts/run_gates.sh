#!/bin/sh
# Usage: run_gates.sh <clone> <receipt-dir>
# Runs the static gates that read the files this PR shares with its
# merge-train predecessors, one receipt per gate, at the clone's HEAD.
set -u
C=$1; OUT=$2
BASE=d47a04ebf2a5193dd06ed4eecf8be00f5c8502ce
cd "$C" || exit 2
run() {
  name=$1; shift
  log=$OUT/gate_$name.log
  { echo "# cmd: $*"; echo "# head: $(git rev-parse HEAD)"; } > "$log"
  "$@" >> "$log" 2>&1
  rc=$?
  echo "# rc=$rc" >> "$log"
  echo "$name rc=$rc"
}
run docs_check_git            python3 -B scripts/docs_check.py
run docs_check_nogit          env GIT_DIR=/nonexistent-r297-4-no-git python3 -B scripts/docs_check.py
run gen_toc_check             python3 -B scripts/gen_toc.py --check
run gen_toc_verify_anchors    python3 -B scripts/gen_toc.py --verify-anchors
run check_em_dash             python3 -B scripts/check_em_dash.py --base "$BASE"
run check_doc_style           python3 -B scripts/check_doc_style.py
run check_doc_paths           python3 -B scripts/check_doc_paths.py
run measure_test_evidence     python3 -B scripts/measure_test_evidence.py --check
run gen_module_matrix_check   python3 -B docs/traceability/gen_module_matrix.py --check
run ci_events_check           python3 -B scripts/ci_events.py --check
run ci_events_selftest        python3 -B scripts/ci_events.py --selftest
run check_rtl_source_lists    python3 -B scripts/check_rtl_source_lists.py
run xvlog_gate_check          python3 -B scripts/xvlog_gate.py --check
run lint_rtl_check            python3 -B scripts/lint_rtl.py --check
run check_sv_idiom            python3 -B scripts/check_sv_idiom.py
run check_cpp_idiom           python3 -B scripts/check_cpp_idiom.py
run check_py_idiom            python3 -B scripts/check_py_idiom.py
run diff_check_composition    git diff --check "$BASE" HEAD
