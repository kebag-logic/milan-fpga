#!/usr/bin/env bash
# gates.sh <clone> <out>: the docs workflow's checks and rtl-fast's light ones, each in the clone, each its own log in
# <out>, a summary line each (name rc last-line) in <out>/SUMMARY.txt. CI plumbing (evidence records, caches, the
# fail-fast watcher, receipts) is left out; the heavy rtl-fast legs run as units of their own.
set -u
L=$1; O=$2
source <scratch>/bin/env.sh
export HOME=<scratch>/home
mkdir -p "$O"; cd "$L"
base=$(git merge-base HEAD 59b098841b1e2826aaf7a38b557faa5345f91c82)
echo "head $(git rev-parse HEAD) status $(git status --porcelain | wc -l) base $base" > "$O/SUMMARY.txt"
run() {
  local name=$1; shift
  timeout 1800 "$@" > "$O/$name.log" 2>&1
  local rc=$?
  printf '%-34s rc=%s  %s\n' "$name" "$rc" "$(tail -1 "$O/$name.log" | cut -c1-150)" >> "$O/SUMMARY.txt"
}
run wire_accountability python3 scripts/check_wire_accountability.py --self-test
run docs_check python3 scripts/docs_check.py
run feature_status python3 scripts/check_feature_status.py
run feature_status_st python3 scripts/check_feature_status.py --self-test
MDPY=<data>/tools/md-venv-40cdefe08ebd/bin/python3   # the pinned pyslang and Markdown renderer
run hdl_reference_st $MDPY scripts/gen_hdl_reference.py --selftest
run hdl_reference $MDPY scripts/gen_hdl_reference.py --output "$O/hdl-reference"
run em_dash $MDPY scripts/check_em_dash.py --base "$base"
run em_dash_st $MDPY scripts/check_em_dash.py --selftest
run doc_style python3 scripts/check_doc_style.py
run doc_style_st python3 scripts/check_doc_style.py --selftest
run gptp_docs python3 scripts/check_gptp_docs.py
run gptp_docs_st python3 scripts/check_gptp_docs.py --selftest
run gptp_docs_sub python3 scripts/check_gptp_docs.py --with-submodule
run solution_docs python3 scripts/check_solution_docs.py
run solution_docs_st python3 scripts/check_solution_docs.py --selftest
run submodule_docs python3 scripts/check_submodule_docs.py
run submodule_docs_st python3 scripts/check_submodule_docs.py --selftest
run diagram_pngs python3 scripts/check_diagram_pngs.py
run control_flow_st python3 scripts/measure_control_flow.py --selftest
run cohesion_st python3 scripts/measure_cohesion.py --selftest
run baremetal python3 scripts/check_baremetal_only.py --check
run baremetal_st python3 scripts/check_baremetal_only.py --selftest
run nvm_record_space python3 scripts/check_nvm_record_space.py
run nvm_record_space_st python3 scripts/check_nvm_record_space.py --self-test
run nvm_capture python3 scripts/check_nvm_capture.py
run soc_sources python3 scripts/check_soc_sources.py
run soc_sources_st python3 scripts/check_soc_sources.py --selftest
run rtl_source_lists python3 scripts/check_rtl_source_lists.py
run rtl_source_lists_st python3 scripts/check_rtl_source_lists.py --selftest
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
run test_evidence_readers python3 scripts/measure_test_evidence_readers.py --check
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
run toc_st $MDPY scripts/gen_toc.py --selftest
run toc_anchors $MDPY scripts/gen_toc.py --verify-anchors
run toc $MDPY scripts/gen_toc.py --check
run docs_inventory $MDPY scripts/docs_inventory.py --check
run docs_inventory_st $MDPY scripts/docs_inventory.py --selftest
run sweep_shape_st python3 scripts/check_sweep_shape.py --self-test
run deploy_shape_st python3 scripts/check_deploy_shape.py --self-test
run entity_shape_st python3 scripts/check_entity_shape.py --self-test
run register_reference python3 scripts/gen_register_reference.py --check
run register_reference_st python3 scripts/gen_register_reference.py --selftest
run gate_workflows python3 scripts/ci_gate_workflows.py --check
run ci_events python3 scripts/ci_events.py --check
run ci_events_st python3 scripts/ci_events.py --selftest
run lint_rtl python3 scripts/lint_rtl.py --check --self-test --jobs 4
run xvlog python3 scripts/xvlog_gate.py --check
run pp_srcs python3 scripts/pp_srcs.py --check --selftest
run gen_mailbox python3 -B sw/mailbox/gen_mailbox.py --check
run gen_mailbox_cross python3 -B sw/mailbox/gen_mailbox.py --crosscheck
run gen_mailbox_st python3 -B sw/mailbox/gen_mailbox.py --selftest
run module_matrix python3 docs/traceability/gen_module_matrix.py --check
echo "GATES_DONE $(date -Iseconds)" >> "$O/SUMMARY.txt"
