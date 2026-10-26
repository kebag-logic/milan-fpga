#!/usr/bin/env bash
# Run the exact-head CI-tooling and docs gates concurrently; one log and rc file per gate.
# Usage: run_gates.sh <worktree> <outdir>
set -u
wt=$1; out=$2; mkdir -p "$out"; cd "$wt"
gates=(
 "ci_gate_workflows_check|python3 scripts/ci_gate_workflows.py --check"
 "ci_gate_workflows_selftest|python3 scripts/ci_gate_workflows_selftest.py"
 "ci_case_receipts_selftest|python3 scripts/ci_case_receipts_selftest.py"
 "ci_make_cases_selftest|python3 scripts/ci_make_cases_selftest.py"
 "ci_maap_cases_selftest|python3 scripts/ci_maap_cases_selftest.py"
 "ci_capture_cases_selftest|python3 scripts/ci_capture_cases_selftest.py"
 "ci_suite_pieces_selftest|python3 scripts/ci_suite_pieces_selftest.py"
 "ci_suite_collect_selftest|python3 scripts/ci_suite_collect_selftest.py"
 "ci_fail_fast_selftest|python3 scripts/ci_fail_fast_selftest.py"
 "ci_runtime_evidence_selftest|python3 scripts/ci_runtime_evidence_selftest.py"
 "ci_install_cache_selftest|python3 scripts/ci_install_cache_selftest.py"
 "generate_ci_evidence_pins_check|python3 scripts/generate_ci_evidence_pins.py --check"
 "ci_workflow_plan_selftest|python3 scripts/ci_workflow_plan_selftest.py"
 "ci_manifest_selftest|python3 scripts/ci_manifest_selftest.py"
 "ci_scope_selftest|python3 scripts/ci_scope.py --selftest"
 "ci_events_check|python3 scripts/ci_events.py --check"
 "ci_events_selftest|python3 scripts/ci_events.py --selftest"
 "docs_check|python3 scripts/docs_check.py"
 "check_em_dash|python3 scripts/check_em_dash.py --base 76de691e5625cc4ea2f9a19def9e07c1183a14ee"
 "check_doc_style|python3 scripts/check_doc_style.py"
 "gen_toc_check|python3 scripts/gen_toc.py --check"
 "check_doc_paths|python3 scripts/check_doc_paths.py"
 "check_py_idiom|python3 scripts/check_py_idiom.py"
)
for g in "${gates[@]}"; do
  n=${g%%|*}; c=${g#*|}
  ( start=$(date +%s); bash -c "$c" > "$out/$n.log" 2>&1; rc=$?; echo "$rc $(( $(date +%s)-start ))s $c" > "$out/$n.rc" ) &
  while [ "$(jobs -rp | wc -l)" -ge 16 ]; do sleep 1; done
done
wait
for f in "$out"/*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
