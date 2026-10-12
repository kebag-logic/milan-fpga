#!/usr/bin/env bash
# Scratch: run the docs job's repository gates from a tree with one interpreter, one log per command.
# usage: docsjob.sh <tree> <log directory> <python> <em-dash base>
set -u
tree=$1; logs=$2; py=$3; base=$4
mkdir -p "$logs"
cd "$tree" || exit 2
fail=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  name=$(printf '%s' "$cmd" | tr ' /' '__')
  eval "$py $cmd" > "$logs/$name.log" 2>&1
  rc=$?
  printf 'rc=%d %s\n' "$rc" "$cmd"
  [ "$rc" -ne 0 ] && fail=1
done <<LIST
docs/diagrams/submodule_boundaries.gen.py --check
docs/diagrams/submodule_boundaries.gen.py --selftest
docs/DOC_MAP.gen.py --check
docs/DOC_MAP.gen.py --selftest
docs/traceability/gen_module_matrix.py --check
scripts/check_archive.py
scripts/check_archive.py --selftest
scripts/check_baremetal_only.py --check
scripts/check_baremetal_only.py --selftest
scripts/check_cpp_idiom.py
scripts/check_cpp_idiom.py --selftest
scripts/check_diagram_pngs.py
scripts/check_diagram_pngs.py --selftest
scripts/check_doc_paths.py
scripts/check_doc_style.py
scripts/check_doc_style.py --selftest
scripts/check_em_dash.py --base $base
scripts/check_feature_status.py
scripts/check_feature_status.py --self-test
scripts/check_gptp_docs.py
scripts/check_gptp_docs.py --selftest
scripts/check_hygiene.py --check
scripts/check_hygiene.py --selftest
scripts/check_port_contracts.py
scripts/check_port_contracts.py --selftest
scripts/check_py_idiom.py
scripts/check_py_idiom.py --selftest
scripts/check_rtl_source_lists.py
scripts/check_rtl_source_lists.py --selftest
scripts/check_sh_idiom.py
scripts/check_sh_idiom.py --selftest
scripts/check_solution_docs.py
scripts/check_solution_docs.py --selftest
scripts/check_submodule_docs.py
scripts/check_submodule_docs.py --selftest
scripts/check_sv_idiom.py
scripts/check_sv_idiom.py --selftest
scripts/check_todo_ownership.py
scripts/check_todo_ownership.py --selftest
scripts/ci_events.py --check
scripts/ci_events.py --selftest
scripts/ci_scope.py --selftest
scripts/docs_check.py
scripts/gen_toc.py --check
scripts/gen_toc.py --selftest
scripts/gen_toc.py --verify-anchors
scripts/measure_cohesion.py --selftest
scripts/measure_control_flow.py --selftest
scripts/measure_fail_fast.py --check
scripts/measure_fail_fast.py --selftest
scripts/measure_naming.py --check
scripts/measure_naming.py --selftest
scripts/measure_test_evidence.py --check
scripts/measure_test_evidence.py --selftest
LIST
exit $fail
