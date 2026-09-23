#!/usr/bin/env bash
# Run the focused documentation gates for #437 at a checkout, one receipt per command.
# Usage: run_gates.sh <checkout> <receipt-dir> <base-rev>
set -u
repo=$1 out=$2 base=$3
mkdir -p "$out"
export PYTHONDONTWRITEBYTECODE=1
cd "$repo" || exit 2
summary="$out/SUMMARY.txt"
: > "$summary"
n=0
run() {
  n=$((n + 1))
  local file
  file=$(printf '%s/%02d.txt' "$out" "$n")
  { printf '$ %s\n' "$*"; printf 'head %s\n' "$(git rev-parse HEAD)"; } > "$file"
  "$@" >> "$file" 2>&1
  local rc=$?
  printf 'exit %d\n' "$rc" >> "$file"
  printf '%02d exit=%d %s\n' "$n" "$rc" "$*" >> "$summary"
}
run python3 scripts/gen_toc.py --selftest
run python3 scripts/gen_toc.py --check
run python3 scripts/gen_toc.py --verify-anchors
run python3 scripts/check_em_dash.py --selftest
run python3 scripts/check_em_dash.py --base "$base"
run python3 scripts/docs_check.py
run python3 scripts/docs_check.py --selftest
run python3 scripts/check_doc_style.py
run python3 scripts/check_doc_style.py --selftest
run python3 scripts/check_py_idiom.py
run python3 scripts/check_py_idiom.py --selftest
run python3 scripts/check_hygiene.py --check
run python3 scripts/check_hygiene.py --selftest
run python3 scripts/check_todo_ownership.py
run python3 scripts/check_todo_ownership.py --selftest
run python3 scripts/measure_control_flow.py --selftest
run python3 scripts/measure_cohesion.py --selftest
run python3 scripts/measure_naming.py --check
run python3 scripts/measure_naming.py --selftest
run python3 scripts/measure_fail_fast.py --check
run python3 scripts/measure_fail_fast.py --selftest
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/measure_test_evidence.py --selftest
run python3 scripts/check_doc_paths.py
run python3 docs/DOC_MAP.gen.py --check
run python3 scripts/check_archive.py
run git diff --check "$base" HEAD
run git status --porcelain --untracked-files=all
cat "$summary"
