#!/bin/sh
# Documentation and source-list gates the M7 diff touches, each with its own
# log and rc, run from the review clone. Usage: doc_gates.sh <clone> <out>
set -u
C=$1; OUT=$2
MDPY=$VALIDATION_TOOLS/md-venv/bin/python3
PY312=$VALIDATION_TOOLS/uvpy/cpython-3.12.3-linux-x86_64-gnu/bin/python3
BASE=e8454e2751d05b02ee8e5a571857589ab358ab86
mkdir -p "$OUT"
cd "$C" || exit 2
g() {
  name=$1; shift
  "$@" > "$OUT/$name.log" 2>&1
  echo "$?" > "$OUT/$name.rc"
  printf '%s\t%s\t%s\n' "$name" "$(cat "$OUT/$name.rc")" "$*"
}
g docs_check $MDPY scripts/docs_check.py
g em_dash $MDPY scripts/check_em_dash.py --base $BASE
g doc_style $MDPY scripts/check_doc_style.py
g toc_check $MDPY scripts/gen_toc.py --check
g toc_anchors $MDPY scripts/gen_toc.py --verify-anchors
g doc_paths $MDPY scripts/check_doc_paths.py
g doc_map $MDPY docs/DOC_MAP.gen.py --check
g module_matrix $MDPY docs/traceability/gen_module_matrix.py --check
g gptp_docs_sub $MDPY scripts/check_gptp_docs.py --with-submodule
g submodule_docs $MDPY scripts/check_submodule_docs.py
g submodule_diagram $MDPY docs/diagrams/submodule_boundaries.gen.py --check
g timesync $MDPY docs/diagrams/timesync_chain.gen.py --check
g diagram_pngs $MDPY scripts/check_diagram_pngs.py
g rtl_source_lists $PY312 scripts/check_rtl_source_lists.py
g ci_scope_self $PY312 scripts/ci_scope.py --selftest
g test_evidence $PY312 scripts/measure_test_evidence.py --check
g py_idiom $PY312 scripts/check_py_idiom.py
g cpp_idiom $PY312 scripts/check_cpp_idiom.py
g sv_idiom $PY312 scripts/check_sv_idiom.py
g hygiene $PY312 scripts/check_hygiene.py --check
g resource_baseline $PY312 syn/ooc/pp_resource_gate.py check-baseline
g one_valued_check $PY312 scripts/gen_one_valued_table.py --check
g diff_base git diff --check $BASE HEAD
