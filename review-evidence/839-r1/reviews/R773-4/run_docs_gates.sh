#!/bin/bash
# Usage: run_docs_gates.sh <repo> <receipt-dir> <base-sha>
# Runs the docs workflow's repository-owned gate commands (no installs) and records rc per command.
repo=$1; out=$2; base=$3
cd "$repo" || exit 2
: > "$out/docs_gates.tsv"
run() { local name=$1; shift; "$@" > "$out/docs_$name.log" 2>&1; local rc=$?; printf '%s\t%s\t%s\n' "$rc" "$name" "$*" >> "$out/docs_gates.tsv"; }
run wire_acct python3 scripts/check_wire_accountability.py --self-test
run docs_check python3 scripts/docs_check.py
run feature_status python3 scripts/check_feature_status.py
run em_dash python3 scripts/check_em_dash.py --base "$base"
run doc_style python3 scripts/check_doc_style.py
run doc_style_st python3 scripts/check_doc_style.py --selftest
run gptp_docs python3 scripts/check_gptp_docs.py
run gptp_docs_st python3 scripts/check_gptp_docs.py --selftest
run doc_map python3 docs/DOC_MAP.gen.py --check
run doc_map_st python3 docs/DOC_MAP.gen.py --selftest
run timesync python3 docs/diagrams/timesync_chain.gen.py --check
run timesync_st python3 docs/diagrams/timesync_chain.gen.py --selftest
run solution python3 scripts/check_solution_docs.py
run solution_st python3 scripts/check_solution_docs.py --selftest
run submod_diag python3 docs/diagrams/submodule_boundaries.gen.py --check
run submod_diag_st python3 docs/diagrams/submodule_boundaries.gen.py --selftest
run submod_docs python3 scripts/check_submodule_docs.py
run submod_docs_st python3 scripts/check_submodule_docs.py --selftest
run diagram_pngs python3 scripts/check_diagram_pngs.py
run diagram_pngs_st python3 scripts/check_diagram_pngs.py --selftest
run feature_status_st python3 scripts/check_feature_status.py --self-test
run trace_matrix python3 docs/traceability/gen_module_matrix.py --check
run gptp_docs_sub python3 scripts/check_gptp_docs.py --with-submodule
run measure_cf_st python3 scripts/measure_control_flow.py --selftest
run measure_coh_st python3 scripts/measure_cohesion.py --selftest
run baremetal_only python3 scripts/check_baremetal_only.py --check
run baremetal_only_st python3 scripts/check_baremetal_only.py --selftest
run nvm_space python3 scripts/check_nvm_record_space.py
run nvm_space_st python3 scripts/check_nvm_record_space.py --self-test
run nvm_capture python3 scripts/check_nvm_capture.py
run nvm_fw_st python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
run soc_sources python3 scripts/check_soc_sources.py
run soc_sources_st python3 scripts/check_soc_sources.py --selftest
run iob_pack_st python3 sw/litex/iob_pack_selftest.py
run rtl_lists python3 scripts/check_rtl_source_lists.py
run rtl_lists_st python3 scripts/check_rtl_source_lists.py --selftest
run naming python3 scripts/measure_naming.py --check
run naming_st python3 scripts/measure_naming.py --selftest
run port_contracts python3 scripts/check_port_contracts.py
run port_contracts_st python3 scripts/check_port_contracts.py --selftest
run fail_fast python3 scripts/measure_fail_fast.py --check
run fail_fast_st python3 scripts/measure_fail_fast.py --selftest
run todo python3 scripts/check_todo_ownership.py
run todo_st python3 scripts/check_todo_ownership.py --selftest
run test_evidence python3 scripts/measure_test_evidence.py --check
run test_evidence_st python3 scripts/measure_test_evidence.py --selftest
run hygiene python3 scripts/check_hygiene.py --check
run hygiene_st python3 scripts/check_hygiene.py --selftest
run sv_idiom python3 scripts/check_sv_idiom.py
run sv_idiom_st python3 scripts/check_sv_idiom.py --selftest
run cpp_idiom python3 scripts/check_cpp_idiom.py
run cpp_idiom_st python3 scripts/check_cpp_idiom.py --selftest
run py_idiom python3 scripts/check_py_idiom.py
run py_idiom_st python3 scripts/check_py_idiom.py --selftest
run sh_idiom python3 scripts/check_sh_idiom.py
run sh_idiom_st python3 scripts/check_sh_idiom.py --selftest
run doc_paths python3 scripts/check_doc_paths.py
run archive python3 scripts/check_archive.py
run archive_st python3 scripts/check_archive.py --selftest
run toc_st python3 scripts/gen_toc.py --selftest
run toc_anchors python3 scripts/gen_toc.py --verify-anchors
run toc python3 scripts/gen_toc.py --check
run inventory python3 scripts/docs_inventory.py --check
run inventory_st python3 scripts/docs_inventory.py --selftest
run aem_store_st python3 avdecc/gen_aem_store.py --self-test
run sweep_shape_st python3 scripts/check_sweep_shape.py --self-test
run deploy_shape_st python3 scripts/check_deploy_shape.py --self-test
run entity_shape_st python3 scripts/check_entity_shape.py --self-test
run ci_gate_wf python3 scripts/ci_gate_workflows.py --check
run ci_gate_wf_st python3 scripts/ci_gate_workflows_selftest.py
run ci_case_receipts_st python3 scripts/ci_case_receipts_selftest.py
run ci_make_cases_st python3 scripts/ci_make_cases_selftest.py
run ci_maap_cases_st python3 scripts/ci_maap_cases_selftest.py
run ci_capture_cases_st python3 scripts/ci_capture_cases_selftest.py
run ci_suite_pieces_st python3 scripts/ci_suite_pieces_selftest.py
run ci_suite_collect_st python3 scripts/ci_suite_collect_selftest.py
run ci_fail_fast_st python3 scripts/ci_fail_fast_selftest.py
run ci_runtime_ev_st python3 scripts/ci_runtime_evidence_selftest.py
run ci_install_cache_st python3 scripts/ci_install_cache_selftest.py
run ci_evidence_pins python3 scripts/generate_ci_evidence_pins.py --check
run ci_wf_plan_st python3 scripts/ci_workflow_plan_selftest.py
run ci_manifest_st python3 scripts/ci_manifest_selftest.py
echo done > "$out/docs_gates.done"
