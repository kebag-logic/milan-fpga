#!/usr/bin/env bash
# Runs the docs workflow's gates (docs.yml, docs-check-no-git and docs-gates-0)
# that need no runner install, one after another, from the repository root
# given as $1; prints each command's exit status and a total. The pinned
# markdown renderer is added through PYTHONPATH ($2, its site-packages).
set -u
cd "$1" || exit 2
export PYTHONPATH="$2"
base="$(git merge-base e76a755afc0536453161e3cd33f6f4d2dcd7641f HEAD)"
failed=0
run() {
    "$@"
    local rc=$?
    echo "[rc=$rc] $*"
    [ "$rc" -eq 0 ] || failed=$((failed + 1))
}
run python3 scripts/check_wire_accountability.py --self-test
run python3 scripts/docs_check.py
run python3 scripts/check_feature_status.py
run python3 scripts/gen_hdl_reference.py --selftest
run python3 scripts/gen_hdl_reference.py --output "$(mktemp -d)"
run python3 scripts/check_em_dash.py --base "$base"
run python3 scripts/check_em_dash.py --selftest
run python3 scripts/check_doc_style.py
run python3 scripts/check_doc_style.py --selftest
run python3 scripts/check_gptp_docs.py
run python3 scripts/check_gptp_docs.py --selftest
run python3 docs/DOC_MAP.gen.py --check
run python3 docs/DOC_MAP.gen.py --selftest
run python3 docs/diagrams/timesync_chain.gen.py --check
run python3 docs/diagrams/timesync_chain.gen.py --selftest
run python3 scripts/check_solution_docs.py
run python3 scripts/check_solution_docs.py --selftest
run python3 docs/diagrams/submodule_boundaries.gen.py --check
run python3 docs/diagrams/submodule_boundaries.gen.py --selftest
run python3 scripts/check_submodule_docs.py
run python3 scripts/check_submodule_docs.py --selftest
run python3 scripts/check_diagram_pngs.py
run python3 scripts/check_diagram_pngs.py --selftest
run python3 scripts/check_feature_status.py --self-test
run python3 docs/traceability/gen_module_matrix.py --check
run python3 scripts/measure_control_flow.py --selftest
run python3 scripts/measure_cohesion.py --selftest
run python3 scripts/check_baremetal_only.py --check
run python3 scripts/check_baremetal_only.py --selftest
run python3 scripts/check_nvm_record_space.py
run python3 scripts/check_nvm_record_space.py --self-test
run python3 scripts/check_nvm_capture.py
run python3 scripts/check_soc_sources.py
run python3 scripts/check_soc_sources.py --selftest
run python3 sw/litex/iob_pack_selftest.py
run python3 scripts/check_rtl_source_lists.py
run python3 scripts/check_rtl_source_lists.py --selftest
run python3 scripts/measure_naming.py --check
run python3 scripts/measure_naming.py --selftest
run python3 scripts/check_port_contracts.py
run python3 scripts/check_port_contracts.py --selftest
run python3 scripts/measure_fail_fast.py --check
run python3 scripts/measure_fail_fast.py --selftest
run python3 scripts/check_todo_ownership.py
run python3 scripts/check_todo_ownership.py --selftest
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/measure_test_evidence.py --selftest
run python3 scripts/check_hygiene.py --check
run python3 scripts/check_hygiene.py --selftest
run python3 scripts/check_sv_idiom.py
run python3 scripts/check_sv_idiom.py --selftest
run python3 scripts/check_cpp_idiom.py
run python3 scripts/check_cpp_idiom.py --selftest
run python3 scripts/check_py_idiom.py
run python3 scripts/check_py_idiom.py --selftest
run python3 scripts/check_sh_idiom.py
run python3 scripts/check_sh_idiom.py --selftest
run python3 scripts/check_doc_paths.py
run python3 scripts/check_archive.py
run python3 scripts/check_archive.py --selftest
run python3 scripts/gen_toc.py --selftest
run python3 scripts/gen_toc.py --verify-anchors
run python3 scripts/gen_toc.py --check
run python3 avdecc/gen_aem_store.py --self-test
run python3 scripts/check_sweep_shape.py --self-test
run python3 scripts/check_deploy_shape.py --self-test
run python3 scripts/check_entity_shape.py --self-test
run python3 scripts/ci_gate_workflows.py --check
run python3 scripts/ci_events.py --check
echo "docs gates: $failed failed"
exit $((failed > 0))
