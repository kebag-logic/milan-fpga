#!/usr/bin/env bash
# Static/Markdown gates that read the composed files, in the pinned Markdown venv.
# Usage: run_static_gates.sh <clone> <packet> <venv-python>
set -u
CLONE=$1; PKT=$2; PY=$3
cd "$CLONE"
OUT=$PKT/receipts/20_static_gates.tsv; : > "$OUT"
LOGDIR=$PKT/receipts/static_logs; mkdir -p "$LOGDIR"
run() {
  local name=$1; shift
  local log="$LOGDIR/$name.log"
  local t0=$(date +%s)
  "$@" > "$log" 2>&1; local rc=$?
  printf '%s\t%s\t%ss\t%s\t%s\n' "$name" "$rc" "$(( $(date +%s)-t0 ))" "$(sha256sum "$log" | cut -c1-16)" "$*" >> "$OUT"
}
run docs_check                 "$PY" scripts/docs_check.py
run em_dash_base_C602          "$PY" scripts/check_em_dash.py --base a3f95a4cea1faa3470b65b4ffc8a9bb3dc1b0c9c
run em_dash_base_dev           "$PY" scripts/check_em_dash.py --base 7390b43627032c71c470e2aa8d0845eb5b740663
run gen_toc_selftest           "$PY" scripts/gen_toc.py --selftest
run gen_toc_verify_anchors     "$PY" scripts/gen_toc.py --verify-anchors
run gen_toc_check              "$PY" scripts/gen_toc.py --check
run doc_style                  "$PY" scripts/check_doc_style.py
run doc_style_selftest         "$PY" scripts/check_doc_style.py --selftest
run gptp_docs                  "$PY" scripts/check_gptp_docs.py
run doc_map_check              "$PY" docs/DOC_MAP.gen.py --check
run solution_docs              "$PY" scripts/check_solution_docs.py
run submodule_docs             "$PY" scripts/check_submodule_docs.py
run diagram_pngs               "$PY" scripts/check_diagram_pngs.py
run baremetal_only             "$PY" scripts/check_baremetal_only.py --check
run soc_sources                "$PY" scripts/check_soc_sources.py
run soc_sources_selftest       "$PY" scripts/check_soc_sources.py --selftest
run rtl_source_lists           "$PY" scripts/check_rtl_source_lists.py
run measure_naming             "$PY" scripts/measure_naming.py --check
run port_contracts             "$PY" scripts/check_port_contracts.py
run measure_fail_fast          "$PY" scripts/measure_fail_fast.py --check
run todo_ownership             "$PY" scripts/check_todo_ownership.py
run measure_test_evidence      "$PY" scripts/measure_test_evidence.py --check
run hygiene                    "$PY" scripts/check_hygiene.py --check
run sv_idiom                   "$PY" scripts/check_sv_idiom.py
run cpp_idiom                  "$PY" scripts/check_cpp_idiom.py
run py_idiom                   "$PY" scripts/check_py_idiom.py
run sh_idiom                   "$PY" scripts/check_sh_idiom.py
run ci_events_check            "$PY" scripts/ci_events.py --check
run ci_events_selftest         "$PY" scripts/ci_events.py --selftest
run archive                    "$PY" scripts/check_archive.py
run feature_status             "$PY" scripts/check_feature_status.py
run nvm_record_space           "$PY" scripts/check_nvm_record_space.py
run wire_accountability_self   "$PY" scripts/check_wire_accountability.py --self-test
run iob_pack_selftest          "$PY" sw/litex/iob_pack_selftest.py
cat "$OUT"
