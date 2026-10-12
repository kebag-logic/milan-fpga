#!/bin/sh
# Runs the docs-workflow gates that need no network, SDK, act, or submodule write.
# Usage: docs_gates.sh REPO OUTDIR ; writes OUTDIR/docs_gates.tsv
R=$1; O=$2; cd "$R" || exit 2
T=$O/docs_gates.tsv; : > $T
run() { name=$1; shift; "$@" > "$O/gate_$name.log" 2>&1; printf '%s\t%s\t%s\n' "$name" "$?" "$*" >> $T; }
run docs_check python3 scripts/docs_check.py
run em_dash python3 scripts/check_em_dash.py --base c6bd08c6
run doc_style python3 scripts/check_doc_style.py
run doc_style_st python3 scripts/check_doc_style.py --selftest
run gptp_docs python3 scripts/check_gptp_docs.py
run doc_map python3 docs/DOC_MAP.gen.py --check
run timesync python3 docs/diagrams/timesync_chain.gen.py --check
run solution python3 scripts/check_solution_docs.py
run submod_diag python3 docs/diagrams/submodule_boundaries.gen.py --check
run submod_docs python3 scripts/check_submodule_docs.py
run diagram_pngs python3 scripts/check_diagram_pngs.py
run feature_status_st python3 scripts/check_feature_status.py --self-test
run feature_status python3 scripts/check_feature_status.py
run module_matrix python3 docs/traceability/gen_module_matrix.py --check
run gptp_docs_sub python3 scripts/check_gptp_docs.py --with-submodule
run control_flow_st python3 scripts/measure_control_flow.py --selftest
run cohesion_st python3 scripts/measure_cohesion.py --selftest
run baremetal python3 scripts/check_baremetal_only.py --check
run nvm_record python3 scripts/check_nvm_record_space.py
run nvm_capture python3 scripts/check_nvm_capture.py
run soc_sources python3 scripts/check_soc_sources.py
run rtl_srclists python3 scripts/check_rtl_source_lists.py
run naming python3 scripts/measure_naming.py --check
run naming_st python3 scripts/measure_naming.py --selftest
run port_contracts python3 scripts/check_port_contracts.py
run fail_fast python3 scripts/measure_fail_fast.py --check
run todo python3 scripts/check_todo_ownership.py
run test_evidence python3 scripts/measure_test_evidence.py --check
run test_evidence_st python3 scripts/measure_test_evidence.py --selftest
run hygiene python3 scripts/check_hygiene.py --check
run sv_idiom python3 scripts/check_sv_idiom.py
run cpp_idiom python3 scripts/check_cpp_idiom.py
run cpp_idiom_st python3 scripts/check_cpp_idiom.py --selftest
run py_idiom python3 scripts/check_py_idiom.py
run py_idiom_st python3 scripts/check_py_idiom.py --selftest
run sh_idiom python3 scripts/check_sh_idiom.py
run ci_events python3 scripts/ci_events.py --check
run doc_paths python3 scripts/check_doc_paths.py
run archive python3 scripts/check_archive.py
run toc_anchors python3 scripts/gen_toc.py --verify-anchors
run toc_check python3 scripts/gen_toc.py --check
run aem_store_st python3 avdecc/gen_aem_store.py --self-test
run wire_acct_st python3 scripts/check_wire_accountability.py --self-test
run pp_srcs python3 scripts/pp_srcs.py --check --selftest
run lint_rtl python3 scripts/lint_rtl.py --check
run diff_check git diff --check c6bd08c6 HEAD
