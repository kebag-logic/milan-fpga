#!/usr/bin/env bash
# Run the gates PR #638 touches at round 3, in parallel, one log and one rc file each.
# Usage: run_gates.sh <repo checkout> <output dir> <markdown venv python> <base sha>
set -u
repo=$1 out=$2 mdpy=$3 base=$4
mkdir -p "$out"
cd "$repo" || exit 2
jobs=(
  "gate_selftest|python3 syn/ooc/pp_resource_gate.py --selftest"
  "gate_mutants|python3 syn/ooc/pp_resource_gate_mutants.py"
  "gate_check_baseline|python3 syn/ooc/pp_resource_gate.py check-baseline"
  "pp_baseline_selftest|python3 syn/ooc/pp_baseline.py --selftest"
  "pp_baseline_mutants|python3 syn/ooc/pp_baseline_mutants.py"
  "pp_baseline_reports_selftest|python3 syn/ooc/pp_baseline_reports_selftest.py"
  "dp_srcs_selftest|python3 syn/ooc/dp_srcs.py --selftest"
  "ooc_tcl_selftest|python3 syn/ooc/ooc_tcl_selftest.py"
  "dp_srcs_tops|python3 syn/ooc/dp_srcs.py --top milan_datapath > /dev/null && python3 syn/ooc/dp_srcs.py --top KL_pp_shadow > /dev/null"
  "ci_events|python3 scripts/ci_events.py --check && python3 scripts/ci_events.py --selftest"
  "ci_scope|python3 scripts/ci_scope.py --selftest && git diff --name-only $base HEAD | python3 scripts/ci_scope.py"
  "docs_check|$mdpy scripts/docs_check.py"
  "em_dash|$mdpy scripts/check_em_dash.py --base $base"
  "doc_style|python3 scripts/check_doc_style.py && python3 scripts/check_doc_style.py --selftest"
  "doc_map|python3 docs/DOC_MAP.gen.py --check"
  "solution_docs|python3 scripts/check_solution_docs.py"
  "feature_status|python3 scripts/check_feature_status.py --self-test"
  "module_matrix|python3 docs/traceability/gen_module_matrix.py --check"
  "doc_paths|python3 scripts/check_doc_paths.py"
  "archive|python3 scripts/check_archive.py"
  "toc|$mdpy scripts/gen_toc.py --check && $mdpy scripts/gen_toc.py --verify-anchors"
  "py_idiom|python3 scripts/check_py_idiom.py && python3 scripts/check_py_idiom.py --selftest"
  "hygiene|python3 scripts/check_hygiene.py --check"
  "todo|python3 scripts/check_todo_ownership.py"
  "fail_fast|python3 scripts/measure_fail_fast.py --check"
  "test_evidence|python3 scripts/measure_test_evidence.py --check"
  "diff_check|git diff --check $base HEAD"
  "make43_docs|make --version | head -1 && make -C gptp-processor docs"
  "pp_srcs|python3 scripts/pp_srcs.py --check && python3 scripts/pp_srcs.py --selftest"
  "docs_check_selftest|$mdpy scripts/docs_check.py --selftest"
  "ci_scope_budget_only|echo docs/design/AREA_BUDGET.md | python3 scripts/ci_scope.py"
)
for job in "${jobs[@]}"; do
  name=${job%%|*} cmd=${job#*|}
  ( bash -c "$cmd" > "$out/$name.log" 2>&1; echo $? > "$out/$name.rc" ) &
  while [ "$(jobs -rp | wc -l)" -ge 14 ]; do wait -n; done
done
wait
echo done > "$out/ALL.done"
