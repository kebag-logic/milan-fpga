#!/usr/bin/env bash
# Composition gates for the issue 716 merge-train candidate.
# Usage: gates.sh <clone> <receipts-dir> <markdown-venv-python>
# Runs every gate concurrently (at most 16 at once), one log and one rc file
# per gate, then prints a summary table. Exit status is 0 only if every gate
# returned 0.
set -u
clone=$1 out=$2 md=$3
parent_dev=c6bd08c6f52632c6d33d834ce842ac3cf63f29cc
pr_base=09c7231eca343607c97c0d66abebb2553688712c
mkdir -p "$out"
cd "$clone" || exit 2

gates=(
  "docs_check|$md -B scripts/docs_check.py"
  "docs_check_selftest|$md -B scripts/docs_check.py --selftest"
  "gen_toc_check|$md -B scripts/gen_toc.py --check"
  "gen_toc_verify_anchors|$md -B scripts/gen_toc.py --verify-anchors"
  "gen_toc_selftest|$md -B scripts/gen_toc.py --selftest"
  "em_dash_base_dev_parent|$md -B scripts/check_em_dash.py --base $parent_dev"
  "em_dash_base_pr_base|$md -B scripts/check_em_dash.py --base $pr_base"
  "em_dash_selftest|$md -B scripts/check_em_dash.py --selftest"
  "doc_style|$md -B scripts/check_doc_style.py"
  "doc_style_selftest|$md -B scripts/check_doc_style.py --selftest"
  "doc_paths|$md -B scripts/check_doc_paths.py"
  "doc_map_check|$md -B docs/DOC_MAP.gen.py --check"
  "solution_docs|$md -B scripts/check_solution_docs.py"
  "submodule_docs|$md -B scripts/check_submodule_docs.py"
  "gptp_docs|$md -B scripts/check_gptp_docs.py"
  "ci_events_check|python3 -B scripts/ci_events.py --check"
  "ci_events_selftest|python3 -B scripts/ci_events.py --selftest"
  "ci_events_firmware_census|python3 -B scripts/ci_events.py --firmware-census"
  "ci_scope_selftest|python3 -B scripts/ci_scope.py --selftest"
  "suite_shards_selftest|python3 -B scripts/suite_shards.py --selftest"
  "fw_shards_selftest|python3 -B sw/firmware/ctrl/test/test_ctrl_firmware_shards.py"
  "py_idiom|python3 -B scripts/check_py_idiom.py"
  "py_idiom_selftest|python3 -B scripts/check_py_idiom.py --selftest"
  "hygiene_check|python3 -B scripts/check_hygiene.py --check"
  "test_evidence_check|python3 -B scripts/measure_test_evidence.py --check"
  "naming_check|python3 -B scripts/measure_naming.py --check"
  "fail_fast_check|python3 -B scripts/measure_fail_fast.py --check"
  "todo_ownership|python3 -B scripts/check_todo_ownership.py"
  "nvm_capture|python3 -B scripts/check_nvm_capture.py"
  "diff_check_dev_parent|git diff --check $parent_dev HEAD"
)

run_one() {
  local name=${1%%|*} cmd=${1#*|}
  printf '$ %s\n' "$cmd" > "$out/$name.log"
  bash -c "$cmd" >> "$out/$name.log" 2>&1
  echo $? > "$out/$name.rc"
}
export -f run_one
export out
printf '%s\n' "${gates[@]}" | xargs -P 16 -I{} bash -c 'run_one "$@"' _ {}

fail=0
for g in "${gates[@]}"; do
  name=${g%%|*}
  rc=$(cat "$out/$name.rc")
  printf '%-28s rc=%s  %s\n' "$name" "$rc" "$(tail -n 1 "$out/$name.log" | cut -c1-140)"
  [ "$rc" = 0 ] || fail=1
done
exit $fail
