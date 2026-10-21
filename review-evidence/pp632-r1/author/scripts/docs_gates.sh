#!/usr/bin/env bash
# The documentation workflow's local gates (.github/workflows/docs.yml), run one by one
# from the repository root with each rc recorded. MDPY is a Python with the pinned
# Markdown renderer (tools/markdown/requirements.txt) for the gates that need it.
# usage: docs_gates.sh <out-dir>   (run from the repository root)
set -u
out=$1; mkdir -p "$out"; : > "$out/summary.txt"
MDPY=${MDPY:-python3}
run() {  # name, command...
  local name=$1; shift
  "$@" > "$out/$name.log" 2>&1; local rc=$?
  printf '%-34s rc=%s  %s\n' "$name" "$rc" "$*" >> "$out/summary.txt"
}
run wire_accountability_selftest python3 scripts/check_wire_accountability.py --self-test
run docs_check                python3 scripts/docs_check.py
run feature_status            python3 scripts/check_feature_status.py
run feature_status_selftest   python3 scripts/check_feature_status.py --self-test
run em_dash                   "$MDPY" scripts/check_em_dash.py --base e26f1816
run doc_style                 python3 scripts/check_doc_style.py
run doc_style_selftest        python3 scripts/check_doc_style.py --selftest
run gptp_docs                 python3 scripts/check_gptp_docs.py
run gptp_docs_selftest        python3 scripts/check_gptp_docs.py --selftest
run doc_map                   python3 docs/DOC_MAP.gen.py --check
run doc_map_selftest          python3 docs/DOC_MAP.gen.py --selftest
run timesync_chain            python3 docs/diagrams/timesync_chain.gen.py --check
run timesync_chain_selftest   python3 docs/diagrams/timesync_chain.gen.py --selftest
run solution_docs             python3 scripts/check_solution_docs.py
run solution_docs_selftest    python3 scripts/check_solution_docs.py --selftest
run submodule_boundaries      python3 docs/diagrams/submodule_boundaries.gen.py --check
run submodule_docs            python3 scripts/check_submodule_docs.py
run module_matrix             python3 docs/traceability/gen_module_matrix.py --check
run diagram_pngs              python3 scripts/check_diagram_pngs.py
run diagram_pngs_selftest     python3 scripts/check_diagram_pngs.py --selftest
run test_evidence_selftest    python3 scripts/measure_test_evidence.py --selftest
run measure_cf_selftest       python3 scripts/measure_control_flow.py --selftest
run measure_cohesion_selftest python3 scripts/measure_cohesion.py --selftest
run baremetal_only            python3 scripts/check_baremetal_only.py --check
run nvm_record_space          python3 scripts/check_nvm_record_space.py
run soc_sources               python3 scripts/check_soc_sources.py
run soc_sources_selftest      python3 scripts/check_soc_sources.py --selftest
run rtl_source_lists          python3 scripts/check_rtl_source_lists.py
run rtl_source_lists_selftest python3 scripts/check_rtl_source_lists.py --selftest
run naming                    python3 scripts/measure_naming.py --check
run port_contracts            python3 scripts/check_port_contracts.py
run port_contracts_selftest   python3 scripts/check_port_contracts.py --selftest
run fail_fast                 python3 scripts/measure_fail_fast.py --check
run todo_ownership            python3 scripts/check_todo_ownership.py
run test_evidence             python3 scripts/measure_test_evidence.py --check
run hygiene                   python3 scripts/check_hygiene.py --check
run sv_idiom                  python3 scripts/check_sv_idiom.py
run cpp_idiom                 python3 scripts/check_cpp_idiom.py
run py_idiom                  python3 scripts/check_py_idiom.py
run sh_idiom                  python3 scripts/check_sh_idiom.py
run doc_paths                 python3 scripts/check_doc_paths.py
run archive                   python3 scripts/check_archive.py
run toc_selftest              "$MDPY" scripts/gen_toc.py --selftest
run toc_anchors               "$MDPY" scripts/gen_toc.py --verify-anchors
run toc                       "$MDPY" scripts/gen_toc.py --check
run gate_workflows            python3 scripts/ci_gate_workflows.py --check
run evidence_pins             python3 scripts/generate_ci_evidence_pins.py --check
run suite_shards_selftest     python3 scripts/suite_shards.py --selftest
run pp_srcs                   python3 scripts/pp_srcs.py --check --selftest
# the pinned renderer is recorded by name, not by its host path
sed -i "s#$MDPY #python3 #" "$out/summary.txt"
cat "$out/summary.txt"
