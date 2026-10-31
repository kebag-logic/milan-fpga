#!/usr/bin/env bash
# Run the static gates that read the files the PR and its predecessors both
# changed, on the merge candidate, one log and rc per gate.
# Usage: composition_gates.sh <candidate-clone> <out-dir> <em-dash-base>
set -u
repo=$1; out=$2; base=$3
mkdir -p "$out"
cd "$repo" || exit 2
run() {
  local name=$1; shift
  "$@" > "$out/$name.log" 2>&1
  local rc=$?
  echo "$rc" > "$out/$name.rc"
  printf '%-34s rc=%s\n' "$name" "$rc"
}
run docs_check            python3 scripts/docs_check.py
run feature_status        python3 scripts/check_feature_status.py
run em_dash               python3 scripts/check_em_dash.py --base "$base"
run doc_style             python3 scripts/check_doc_style.py
run doc_paths             python3 scripts/check_doc_paths.py
run toc_verify_anchors    python3 scripts/gen_toc.py --verify-anchors
run toc_check             python3 scripts/gen_toc.py --check
run gptp_docs             python3 scripts/check_gptp_docs.py
run solution_docs         python3 scripts/check_solution_docs.py
run submodule_docs        python3 scripts/check_submodule_docs.py
run archive               python3 scripts/check_archive.py
run nvm_capture           python3 scripts/check_nvm_capture.py
run nvm_record_space      python3 scripts/check_nvm_record_space.py
run soc_sources           python3 scripts/check_soc_sources.py
run rtl_source_lists      python3 scripts/check_rtl_source_lists.py
run port_contracts        python3 scripts/check_port_contracts.py
run naming                python3 scripts/measure_naming.py --check
run fail_fast             python3 scripts/measure_fail_fast.py --check
run test_evidence         python3 scripts/measure_test_evidence.py --check
run hygiene               python3 scripts/check_hygiene.py --check
run todo_ownership        python3 scripts/check_todo_ownership.py
run py_idiom              python3 scripts/check_py_idiom.py
run sh_idiom              python3 scripts/check_sh_idiom.py
run ci_events_check       python3 scripts/ci_events.py --check
run ci_gate_workflows     python3 scripts/ci_gate_workflows.py --check
run litex_sims_selftest   bash scripts/run_litex_sims.sh --selftest
