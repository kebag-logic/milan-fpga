#!/usr/bin/env bash
# Static/document gates that read the files both sides of the composition changed.
# Run from the candidate clone root; receipts land in the packet receipts/ directory.
set -u
here="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="$here/scratch/tool-bin:$PATH"
R="$here/scripts/rcpt.sh"
TRAIN=551e4b5dfa8ac7ec68a3161c95d4000eb6337396
PRHEAD=c6c65e803f9eb270a11dfd65fda5814fb0b0ea55
$R 10_docs_check python3 -B scripts/docs_check.py
$R 11_gen_toc_check python3 scripts/gen_toc.py --check
$R 12_gen_toc_anchors python3 scripts/gen_toc.py --verify-anchors
$R 13_em_dash_vs_train python3 scripts/check_em_dash.py --base $TRAIN
$R 14_em_dash_vs_prhead python3 scripts/check_em_dash.py --base $PRHEAD
$R 15_doc_style python3 scripts/check_doc_style.py
$R 16_doc_paths python3 scripts/check_doc_paths.py
$R 17_ci_events_check python3 scripts/ci_events.py --check
$R 18_ci_events_selftest python3 scripts/ci_events.py --selftest
$R 19_measure_test_evidence python3 scripts/measure_test_evidence.py --check
$R 20_module_matrix python3 docs/traceability/gen_module_matrix.py --check
$R 21_submodule_docs python3 scripts/check_submodule_docs.py
$R 22_submodule_diagram python3 docs/diagrams/submodule_boundaries.gen.py --check
$R 23_diagram_pngs python3 scripts/check_diagram_pngs.py
$R 24_doc_map python3 docs/DOC_MAP.gen.py --check
$R 25_solution_docs python3 scripts/check_solution_docs.py
$R 26_gptp_docs python3 scripts/check_gptp_docs.py
$R 27_feature_status python3 scripts/check_feature_status.py
$R 30_xvlog_gate python3 scripts/xvlog_gate.py --check
$R 31_lint_rtl python3 scripts/lint_rtl.py --check
$R 32_port_contracts python3 scripts/check_port_contracts.py
$R 33_sv_idiom python3 scripts/check_sv_idiom.py
$R 34_cpp_idiom python3 scripts/check_cpp_idiom.py
$R 35_py_idiom python3 scripts/check_py_idiom.py
$R 36_rtl_source_lists python3 scripts/check_rtl_source_lists.py
$R 37_pp_srcs_check python3 scripts/pp_srcs.py --check
$R 38_measure_naming python3 scripts/measure_naming.py --check
$R 39_fail_fast python3 scripts/measure_fail_fast.py --check
$R 40_hygiene python3 scripts/check_hygiene.py --check
$R 41_todo_ownership python3 scripts/check_todo_ownership.py
$R 42_baremetal_only python3 scripts/check_baremetal_only.py --check
$R 43_nvm_capture python3 scripts/check_nvm_capture.py
$R 44_nvm_record_space python3 scripts/check_nvm_record_space.py
$R 45_soc_sources python3 scripts/check_soc_sources.py
$R 46_entity_shape_selftest python3 scripts/check_entity_shape.py --self-test
$R 47_deploy_shape_selftest python3 scripts/check_deploy_shape.py --self-test
$R 48_sweep_shape_selftest python3 scripts/check_sweep_shape.py --self-test
$R 49_wire_accountability python3 scripts/check_wire_accountability.py --self-test
$R 50_git_diff_check_vs_train git diff --check $TRAIN HEAD
$R 51_git_diff_check_vs_prhead git diff --check $PRHEAD HEAD
$R 52_sh_idiom python3 scripts/check_sh_idiom.py
