#!/usr/bin/env bash
# Composition gates for the #539 merge-train candidate. Read-only checks only.
# Usage: run_gates.sh <candidate-clone> <python-with-renderer-lock> <receipt-dir>
set -u
repo=$1; py=$2; out=$3
mkdir -p "$out"
cd "$repo" || exit 2
export PYTHONDONTWRITEBYTECODE=1
parent1=$(git rev-parse HEAD^1)
mbase=$(git merge-base HEAD^1 HEAD^2)
run() {
  local name=$1; shift
  "$@" > "$out/$name.log" 2>&1
  local rc=$?
  printf '%-40s rc=%d  %s\n' "$name" "$rc" "$*" | tee -a "$out/summary.txt"
}
: > "$out/summary.txt"
echo "head=$(git rev-parse HEAD) tree=$(git rev-parse 'HEAD^{tree}') parent1=$parent1 mergebase=$mbase" | tee -a "$out/summary.txt"
run docs_check            "$py" scripts/docs_check.py
run em_dash_parent1       "$py" scripts/check_em_dash.py --base "$parent1"
run em_dash_mergebase     "$py" scripts/check_em_dash.py --base "$mbase"
run em_dash_selftest      "$py" scripts/check_em_dash.py --selftest
run gen_toc_check         "$py" scripts/gen_toc.py --check
run gen_toc_anchors       "$py" scripts/gen_toc.py --verify-anchors
run doc_style             "$py" scripts/check_doc_style.py
run gptp_docs             "$py" scripts/check_gptp_docs.py
run feature_status        "$py" scripts/check_feature_status.py
run feature_status_st     "$py" scripts/check_feature_status.py --self-test
run module_matrix         "$py" docs/traceability/gen_module_matrix.py --check
run doc_paths             "$py" scripts/check_doc_paths.py
run solution_docs         "$py" scripts/check_solution_docs.py
run submodule_docs        "$py" scripts/check_submodule_docs.py
run test_evidence         "$py" scripts/measure_test_evidence.py --check
run test_evidence_st      "$py" scripts/measure_test_evidence.py --selftest
run hygiene               "$py" scripts/check_hygiene.py --check
run sv_idiom              "$py" scripts/check_sv_idiom.py
run cpp_idiom             "$py" scripts/check_cpp_idiom.py
run py_idiom              "$py" scripts/check_py_idiom.py
run sh_idiom              "$py" scripts/check_sh_idiom.py
run naming                "$py" scripts/measure_naming.py --check
run fail_fast             "$py" scripts/measure_fail_fast.py --check
run port_contracts        "$py" scripts/check_port_contracts.py
run todo_ownership        "$py" scripts/check_todo_ownership.py
run rtl_source_lists      "$py" scripts/check_rtl_source_lists.py
run soc_sources           "$py" scripts/check_soc_sources.py
run pp_srcs               "$py" scripts/pp_srcs.py --check
run ci_events_check       "$py" scripts/ci_events.py --check
run ci_events_selftest    "$py" scripts/ci_events.py --selftest
run suite_shards_st       "$py" scripts/suite_shards.py --selftest
run archive               "$py" scripts/check_archive.py
