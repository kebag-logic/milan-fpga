#!/usr/bin/env bash
# Run the documentation workflow's docs-relevant gates on a clean checkout,
# concurrently, one log and one rc file per gate.
# Usage: run_docs_gates.sh <checkout> <python> <out-dir> <base-rev>
set -u
repo=$1 py=$2 out=$3 base=$4
mkdir -p "$out"
cd "$repo" || exit 2

gates=(
  "docs_check|scripts/docs_check.py"
  "feature_status|scripts/check_feature_status.py"
  "feature_status_selftest|scripts/check_feature_status.py --self-test"
  "em_dash|scripts/check_em_dash.py --base $base"
  "em_dash_selftest|scripts/check_em_dash.py --selftest"
  "doc_style|scripts/check_doc_style.py"
  "doc_style_selftest|scripts/check_doc_style.py --selftest"
  "doc_paths|scripts/check_doc_paths.py"
  "gptp_docs|scripts/check_gptp_docs.py"
  "gptp_docs_selftest|scripts/check_gptp_docs.py --selftest"
  "solution_docs|scripts/check_solution_docs.py"
  "submodule_docs|scripts/check_submodule_docs.py"
  "archive|scripts/check_archive.py"
  "hygiene|scripts/check_hygiene.py --check"
  "todo_ownership|scripts/check_todo_ownership.py"
  "gen_toc_selftest|scripts/gen_toc.py --selftest"
  "gen_toc_anchors|scripts/gen_toc.py --verify-anchors"
  "gen_toc_check|scripts/gen_toc.py --check"
  "doc_map_check|docs/DOC_MAP.gen.py --check"
  "traceability_check|docs/traceability/gen_module_matrix.py --check"
)
pids=()
for g in "${gates[@]}"; do
  name=${g%%|*} cmd=${g#*|}
  # shellcheck disable=SC2086
  ( timeout 540 "$py" $cmd >"$out/$name.log" 2>&1; echo $? >"$out/$name.rc" ) &
  pids+=($!)
done
wait "${pids[@]}"
for g in "${gates[@]}"; do
  name=${g%%|*}
  printf '%-26s rc=%s\n' "$name" "$(cat "$out/$name.rc")"
done
