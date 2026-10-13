#!/usr/bin/env bash
# docs_gates.sh <tree> <outfile>: run the documentation/CI-contract gates that read the
# files the composition touches (the docs workflow's commands plus the CI contract
# self-tests), one per line, recording each rc and the tail of its output.
set -u
tree=$1; out=$2
cd "$tree" || exit 2
: > "$out"
fails=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  start=$(date +%s)
  log=$(bash -c "$cmd" 2>&1); rc=$?
  printf '=== rc=%s (%ss) %s\n%s\n' "$rc" "$(( $(date +%s) - start ))" "$cmd" "$(printf '%s\n' "$log" | tail -n 6)" >> "$out"
  [ "$rc" = 0 ] || fails=$((fails+1))
done <<'LIST'
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base ac0142539856222b84ef8e5af414d12132a5bebf
python3 scripts/check_em_dash.py --base e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c
python3 scripts/check_em_dash.py --selftest
python3 scripts/gen_toc.py --selftest
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 scripts/check_gptp_docs.py
python3 scripts/check_doc_paths.py
python3 docs/DOC_MAP.gen.py --check
python3 docs/DOC_MAP.gen.py --selftest
python3 docs/diagrams/timesync_chain.gen.py --check
python3 scripts/check_solution_docs.py
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 docs/diagrams/submodule_boundaries.gen.py --selftest
python3 scripts/check_submodule_docs.py
python3 scripts/check_submodule_docs.py --selftest
python3 scripts/check_diagram_pngs.py
python3 scripts/check_feature_status.py
python3 scripts/check_feature_status.py --self-test
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/ci_events.py --firmware-census
python3 scripts/ci_scope.py --selftest
python3 scripts/suite_shards.py --selftest
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
python3 scripts/measure_test_evidence_readers.py
python3 scripts/check_hygiene.py --check
python3 scripts/check_py_idiom.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_sh_idiom.py
python3 scripts/check_sv_idiom.py
python3 scripts/measure_fail_fast.py --check
python3 scripts/measure_naming.py --check
python3 scripts/check_todo_ownership.py
python3 scripts/check_port_contracts.py
python3 scripts/check_archive.py
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_baremetal_only.py --check
python3 scripts/measure_control_flow.py --selftest
python3 scripts/measure_cohesion.py --selftest
python3 scripts/check_wire_accountability.py --self-test
python3 sw/firmware/ctrl/test/ctrl_build.py --stack-pin
LIST
echo "failures=$fails" >> "$out"
exit $fails
