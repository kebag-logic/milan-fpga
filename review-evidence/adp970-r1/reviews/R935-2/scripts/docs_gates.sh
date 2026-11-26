#!/usr/bin/env bash
# docs_gates.sh - run the docs workflow's local documentation gates on one checkout.
# usage: docs_gates.sh <repo-root> <base-commit> <out-dir> <nogit-copy-dir>
# Each gate's output goes to <out-dir>/<name>.log and its exit status to the summary.
set -u
repo=$1; base=$2; out=$3; nogit=$4
mkdir -p "$out"
cd "$repo" || exit 2
gates=(
  "docs_check|python3 scripts/docs_check.py"
  "em_dash|python3 scripts/check_em_dash.py --base $base"
  "doc_style|python3 scripts/check_doc_style.py && python3 scripts/check_doc_style.py --selftest"
  "gptp_docs|python3 scripts/check_gptp_docs.py && python3 scripts/check_gptp_docs.py --selftest && python3 scripts/check_gptp_docs.py --with-submodule"
  "doc_map|python3 docs/DOC_MAP.gen.py --check && python3 docs/DOC_MAP.gen.py --selftest && python3 docs/diagrams/timesync_chain.gen.py --check"
  "solution_docs|python3 scripts/check_solution_docs.py && python3 scripts/check_solution_docs.py --selftest"
  "submodule_boundaries|python3 docs/diagrams/submodule_boundaries.gen.py --check && python3 docs/diagrams/submodule_boundaries.gen.py --selftest"
  "submodule_docs|python3 scripts/check_submodule_docs.py && python3 scripts/check_submodule_docs.py --selftest"
  "diagram_pngs|python3 scripts/check_diagram_pngs.py && python3 scripts/check_diagram_pngs.py --selftest"
  "feature_status|python3 scripts/check_feature_status.py && python3 scripts/check_feature_status.py --self-test"
  "module_matrix|python3 docs/traceability/gen_module_matrix.py --check"
  "baremetal_only|python3 scripts/check_baremetal_only.py --check"
  "rtl_source_lists|python3 scripts/check_rtl_source_lists.py"
  "naming|python3 scripts/measure_naming.py --check"
  "port_contracts|python3 scripts/check_port_contracts.py"
  "fail_fast|python3 scripts/measure_fail_fast.py --check"
  "todo_ownership|python3 scripts/check_todo_ownership.py"
  "test_evidence|python3 scripts/measure_test_evidence.py --check"
  "hygiene|python3 scripts/check_hygiene.py --check"
  "sv_idiom|python3 scripts/check_sv_idiom.py"
  "cpp_idiom|python3 scripts/check_cpp_idiom.py"
  "py_idiom|python3 scripts/check_py_idiom.py"
  "sh_idiom|python3 scripts/check_sh_idiom.py"
  "doc_paths|python3 scripts/check_doc_paths.py"
  "archive|python3 scripts/check_archive.py"
  "toc|python3 scripts/gen_toc.py --selftest && python3 scripts/gen_toc.py --verify-anchors && python3 scripts/gen_toc.py --check"
  "docs_inventory|python3 scripts/docs_inventory.py --check"
  "register_reference|python3 scripts/gen_register_reference.py --check && python3 docs/diagrams/memory_map.gen.py --check"
  "ci_gate_workflows|python3 scripts/ci_gate_workflows.py --check && python3 scripts/generate_ci_evidence_pins.py --check"
  "wire_accountability|python3 scripts/check_wire_accountability.py --self-test"
)
pids=()
for g in "${gates[@]}"; do
  name=${g%%|*}; cmd=${g#*|}
  ( bash -c "$cmd" > "$out/$name.log" 2>&1; echo $? > "$out/$name.rc" ) &
  pids+=($!)
done
# the no-git job: a copy of the checkout without git metadata
( cd "$nogit" && test ! -e .git && python3 scripts/docs_check.py && python3 scripts/check_feature_status.py ) > "$out/nogit_docs_check.log" 2>&1
echo $? > "$out/nogit_docs_check.rc"
wait "${pids[@]}"
: > "$out/summary.txt"
for f in "$out"/*.rc; do printf '%s %s\n' "$(cat "$f")" "$(basename "$f" .rc)" >> "$out/summary.txt"; done
cat "$out/summary.txt"
