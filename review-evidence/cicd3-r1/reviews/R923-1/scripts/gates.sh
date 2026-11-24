#!/bin/sh
# Run the PR's listed local gates, one after another, in a clean clone at the
# exact head; one log and one exit status per gate.
#   gates.sh CLONE OUTDIR BASE
set -u
clone=$1 out=$2 base=$3
mkdir -p "$out"
cd "$clone" || exit 2
run() {
  name=$1; shift
  start=$(date +%s)
  "$@" > "$out/$name.log" 2>&1
  rc=$?
  echo "$name rc=$rc wall=$(( $(date +%s) - start ))" >> "$out/summary"
}
: > "$out/summary"
run ci_gate_workflows_check python3 scripts/ci_gate_workflows.py --check
run ci_events_check python3 scripts/ci_events.py --check
run ci_gate_workflows_selftest python3 scripts/ci_gate_workflows_selftest.py
run ci_suite_pieces_selftest python3 scripts/ci_suite_pieces_selftest.py
run ci_make_cases_selftest python3 scripts/ci_make_cases_selftest.py
run mutant_stage_selftest python3 scripts/mutant_stage.py --selftest
run gptp_shadow_lifecycle sh -c 'cd tb/verilator/gptp_shadow && python3 test_mutant_lifecycle.py'
run check_py_idiom python3 scripts/check_py_idiom.py
run check_sh_idiom python3 scripts/check_sh_idiom.py
run check_hygiene python3 scripts/check_hygiene.py
run docs_check python3 scripts/docs_check.py
run check_em_dash python3 scripts/check_em_dash.py --base "$base"
run check_doc_paths python3 scripts/check_doc_paths.py
run gen_toc_check python3 scripts/gen_toc.py --check
run ci_fail_fast_selftest python3 scripts/ci_fail_fast_selftest.py
run ci_runtime_evidence_selftest python3 scripts/ci_runtime_evidence_selftest.py
run ci_manifest_selftest python3 scripts/ci_manifest_selftest.py
run ci_workflow_plan_selftest python3 scripts/ci_workflow_plan_selftest.py
run generate_ci_evidence_pins_check python3 scripts/generate_ci_evidence_pins.py --check
run suite_shards_selftest python3 scripts/suite_shards.py --selftest
run test_suite_cancellation python3 scripts/test_suite_cancellation.py
run ci_events_selftest python3 scripts/ci_events.py --selftest
run no_preflight_refused scripts/run_all_suites.sh "$out/np" --no-preflight
echo finished >> "$out/summary"
