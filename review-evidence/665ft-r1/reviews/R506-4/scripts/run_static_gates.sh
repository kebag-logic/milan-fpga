#!/usr/bin/env bash
# Run the documentation and static gates that read the composed files, in
# parallel, at the checkout given as $1. One log and one rc file per gate go
# to $2. Usage: run_static_gates.sh <checkout> <outdir> [em-dash base rev]
set -u
repo=$1; out=$2; base=${3:-5615f52eb810c6104a8250b44004df3a2917cec8}
mkdir -p "$out"; cd "$repo" || exit 2
gates=(
  "docs_check|python3 scripts/docs_check.py"
  "em_dash_base664|python3 scripts/check_em_dash.py --base $base"
  "em_dash_selftest|python3 scripts/check_em_dash.py --selftest"
  "doc_style|python3 scripts/check_doc_style.py"
  "doc_paths|python3 scripts/check_doc_paths.py"
  "doc_map_check|python3 docs/DOC_MAP.gen.py --check"
  "solution_docs|python3 scripts/check_solution_docs.py"
  "submodule_docs|python3 scripts/check_submodule_docs.py"
  "gptp_docs|python3 scripts/check_gptp_docs.py"
  "module_matrix_check|python3 docs/traceability/gen_module_matrix.py --check"
  "feature_status|python3 scripts/check_feature_status.py"
  "toc_selftest|python3 scripts/gen_toc.py --selftest"
  "toc_anchors|python3 scripts/gen_toc.py --verify-anchors"
  "toc_check|python3 scripts/gen_toc.py --check"
  "archive|python3 scripts/check_archive.py"
  "todo_ownership|python3 scripts/check_todo_ownership.py"
  "test_evidence_check|python3 scripts/measure_test_evidence.py --check"
  "test_evidence_selftest|python3 scripts/measure_test_evidence.py --selftest"
  "hygiene_check|python3 scripts/check_hygiene.py --check"
  "cpp_idiom|python3 scripts/check_cpp_idiom.py"
  "py_idiom|python3 scripts/check_py_idiom.py"
  "sh_idiom|python3 scripts/check_sh_idiom.py"
  "naming_check|python3 scripts/measure_naming.py --check"
  "fail_fast_check|python3 scripts/measure_fail_fast.py --check"
  "port_contracts|python3 scripts/check_port_contracts.py"
  "baremetal_only|python3 scripts/check_baremetal_only.py --check"
  "ci_events_check|python3 scripts/ci_events.py --check"
  "ci_events_selftest|python3 scripts/ci_events.py --selftest"
  "ci_scope_selftest|python3 scripts/ci_scope.py --selftest"
  "mailbox_gen_check|python3 sw/mailbox/gen_mailbox.py --check --crosscheck"
  "fw_coverage_selftest|python3 sw/firmware/gtest/fw_coverage_selftest.py"
  "tally_selftest|python3 sw/firmware/gtest/tally_selftest.py"
)
run() { local name=$1 cmd=$2
  ( echo "\$ $cmd"; timeout 900 bash -c "$cmd" ) > "$out/$name.log" 2>&1
  echo $? > "$out/$name.rc"; }
pids=()
for g in "${gates[@]}"; do
  while [ "$(jobs -rp | wc -l)" -ge 16 ]; do wait -n; done
  run "${g%%|*}" "${g#*|}" &
done
wait
for g in "${gates[@]}"; do n=${g%%|*}; printf '%s\t%s\n' "$(cat "$out/$n.rc")" "$n"; done | tee "$out/SUMMARY.tsv"
