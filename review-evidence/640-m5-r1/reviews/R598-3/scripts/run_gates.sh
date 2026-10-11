#!/usr/bin/env bash
# Run the repository's read-only documentation/registry gates on a checkout,
# concurrently, one log and one rc file per gate.
# usage: run_gates.sh <checkout> <out_dir> <parent_rev> <live_dev_rev> <source_base_rev>
set -u
repo=$1; out=$2; parent=$3; dev=$4; srcbase=$5
mkdir -p "$out"
cd "$repo" || exit 2
gates=(
  "docs_check|python3 scripts/docs_check.py"
  "gen_toc_selftest|python3 scripts/gen_toc.py --selftest"
  "gen_toc_check|python3 scripts/gen_toc.py --check"
  "gen_toc_anchors|python3 scripts/gen_toc.py --verify-anchors"
  "em_dash_parent|python3 scripts/check_em_dash.py --base $parent"
  "em_dash_livedev|python3 scripts/check_em_dash.py --base $dev"
  "em_dash_srcbase|python3 scripts/check_em_dash.py --base $srcbase"
  "em_dash_selftest|python3 scripts/check_em_dash.py --selftest"
  "ci_events_check|python3 scripts/ci_events.py --check"
  "ci_events_selftest|python3 scripts/ci_events.py --selftest"
  "test_evidence_check|python3 scripts/measure_test_evidence.py --check"
  "test_evidence_selftest|python3 scripts/measure_test_evidence.py --selftest"
  "doc_style|python3 scripts/check_doc_style.py"
  "doc_paths|python3 scripts/check_doc_paths.py"
  "hygiene_check|python3 scripts/check_hygiene.py --check"
  "py_idiom|python3 scripts/check_py_idiom.py"
  "cpp_idiom|python3 scripts/check_cpp_idiom.py"
  "sv_idiom|python3 scripts/check_sv_idiom.py"
  "todo_ownership|python3 scripts/check_todo_ownership.py"
  "feature_status|python3 scripts/check_feature_status.py"
  "solution_docs|python3 scripts/check_solution_docs.py"
  "submodule_docs|python3 scripts/check_submodule_docs.py"
  "naming_check|python3 scripts/measure_naming.py --check"
  "fail_fast_check|python3 scripts/measure_fail_fast.py --check"
  "rtl_source_lists|python3 scripts/check_rtl_source_lists.py"
  "port_contracts|python3 scripts/check_port_contracts.py"
  "entity_shape_selftest|python3 scripts/check_entity_shape.py --self-test"
  "gptp_docs|python3 scripts/check_gptp_docs.py"
)
for g in "${gates[@]}"; do
  name=${g%%|*}; cmd=${g#*|}
  ( echo "\$ $cmd" > "$out/$name.log"; timeout 900 bash -c "$cmd" >> "$out/$name.log" 2>&1; echo $? > "$out/$name.rc" ) &
done
wait
for g in "${gates[@]}"; do name=${g%%|*}; printf '%-24s rc=%s\n' "$name" "$(cat "$out/$name.rc")"; done
