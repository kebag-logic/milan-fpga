#!/bin/sh
# Run the PR's offline gate commands concurrently at the reviewed checkout.
# Usage: run_offline_gates.sh <checkout> <python3.12.3-with-pyyaml> <receipt-dir>
set -u
repo=$1; py=$2; out=$3
mkdir -p "$out"
cd "$repo" || exit 2
run() { name=$1; shift; ( "$@" >"$out/$name.log" 2>&1; echo $? >"$out/$name.rc" ) & }
run gate_workflows_check  "$py" scripts/ci_gate_workflows.py --check
run ci_events_check       "$py" scripts/ci_events.py --check
run ci_events_selftest    "$py" scripts/ci_events.py --selftest
run gate_workflows_self   "$py" scripts/ci_gate_workflows_selftest.py
run suite_pieces_self     "$py" scripts/ci_suite_pieces_selftest.py
run suite_collect_self    "$py" scripts/ci_suite_collect_selftest.py
run case_receipts_self    "$py" scripts/ci_case_receipts_selftest.py
run fail_fast_self        "$py" scripts/ci_fail_fast_selftest.py
run manifest_self         "$py" scripts/ci_manifest_selftest.py
run runtime_evidence_self "$py" scripts/ci_runtime_evidence_selftest.py
run install_cache_self    "$py" scripts/ci_install_cache_selftest.py
run workflow_plan_self    "$py" scripts/ci_workflow_plan_selftest.py
run make_cases_self       "$py" scripts/ci_make_cases_selftest.py
run maap_cases_self       "$py" scripts/ci_maap_cases_selftest.py
run capture_cases_self    "$py" scripts/ci_capture_cases_selftest.py
run evidence_pins_check   "$py" scripts/generate_ci_evidence_pins.py --check
run suite_shards_self     "$py" scripts/suite_shards.py --selftest
run py_idiom              "$py" scripts/check_py_idiom.py
run hygiene               "$py" scripts/check_hygiene.py
run docs_check            "$py" scripts/docs_check.py
run doc_style             "$py" scripts/check_doc_style.py
run doc_paths             "$py" scripts/check_doc_paths.py
run gen_toc               "$py" scripts/gen_toc.py --check
run em_dash               "$py" scripts/check_em_dash.py --base fa8209889411e8ca95757174c981f720dbcd95a2
wait
for f in "$out"/*.rc; do printf '%s %s\n' "$(cat "$f")" "$(basename "$f" .rc)"; done
