#!/bin/sh
# Static/documentation gates on the composed candidate.
# Usage: run_static_gates.sh <repo> <em-dash-base> <receipt-dir> <python> <verilator-bin-dir>
# Each gate runs in the foreground; its full output and rc go to one receipt.
set -u
REPO=$1; BASE=$2; OUT=$3; PY=$4; VBIN=$5
mkdir -p "$OUT"
export PATH="$VBIN:$PATH"
SUMMARY="$OUT/static_gates_summary.txt"
: > "$SUMMARY"
cd "$REPO" || exit 2
run() {
  name=$1; shift
  log="$OUT/static_$name.log"
  { echo "\$ $*"; echo "head: $(git rev-parse HEAD)"; } > "$log"
  "$@" >> "$log" 2>&1
  rc=$?
  echo "rc=$rc" >> "$log"
  printf '%-44s rc=%s\n' "$name" "$rc" >> "$SUMMARY"
}
run em_dash_vs_parent        "$PY" scripts/check_em_dash.py --base "$BASE"
run em_dash_selftest         "$PY" scripts/check_em_dash.py --selftest
run gen_toc_selftest         "$PY" scripts/gen_toc.py --selftest
run gen_toc_verify_anchors   "$PY" scripts/gen_toc.py --verify-anchors
run gen_toc_check            "$PY" scripts/gen_toc.py --check
run docs_check               "$PY" scripts/docs_check.py
run feature_status           "$PY" scripts/check_feature_status.py
run doc_style                "$PY" scripts/check_doc_style.py
run doc_style_selftest       "$PY" scripts/check_doc_style.py --selftest
run gptp_docs                "$PY" scripts/check_gptp_docs.py
run doc_map_check            "$PY" docs/DOC_MAP.gen.py --check
run timesync_chain_check     "$PY" docs/diagrams/timesync_chain.gen.py --check
run solution_docs            "$PY" scripts/check_solution_docs.py
run submodule_docs           "$PY" scripts/check_submodule_docs.py
run diagram_pngs             "$PY" scripts/check_diagram_pngs.py
run module_matrix_check      "$PY" docs/traceability/gen_module_matrix.py --check
run test_evidence_check      "$PY" scripts/measure_test_evidence.py --check
run test_evidence_selftest   "$PY" scripts/measure_test_evidence.py --selftest
run ci_events_check          "$PY" scripts/ci_events.py --check
run ci_events_selftest       "$PY" scripts/ci_events.py --selftest
run rtl_source_lists         "$PY" scripts/check_rtl_source_lists.py
run port_contracts           "$PY" scripts/check_port_contracts.py
run naming_check             "$PY" scripts/measure_naming.py --check
run fail_fast_check          "$PY" scripts/measure_fail_fast.py --check
run todo_ownership           "$PY" scripts/check_todo_ownership.py
run hygiene_check            "$PY" scripts/check_hygiene.py --check
run sv_idiom                 "$PY" scripts/check_sv_idiom.py
run cpp_idiom                "$PY" scripts/check_cpp_idiom.py
run py_idiom                 "$PY" scripts/check_py_idiom.py
run sh_idiom                 "$PY" scripts/check_sh_idiom.py
run archive                  "$PY" scripts/check_archive.py
run soc_sources              "$PY" scripts/check_soc_sources.py
run baremetal_only           "$PY" scripts/check_baremetal_only.py --check
run nvm_record_space         "$PY" scripts/check_nvm_record_space.py
run pp_srcs_check            "$PY" scripts/pp_srcs.py --check
run lint_rtl_check           "$PY" scripts/lint_rtl.py --check
cat "$SUMMARY"
