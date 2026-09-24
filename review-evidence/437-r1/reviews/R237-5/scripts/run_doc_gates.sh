#!/usr/bin/env bash
# Run the documentation gates PR #538 touches, from a clone at the reviewed
# head, with a given interpreter that has tools/markdown/requirements.txt
# installed. Usage: run_doc_gates.sh <clone> <python> <base-sha>
# Prints one line per command: [rc=N] command :: last output line.
set -uo pipefail
clone=$1 py=$2 base=$3
cd "$clone" || exit 2
export PYTHONDONTWRITEBYTECODE=1
cmds=(
  "scripts/gen_toc.py --selftest"
  "scripts/gen_toc.py --check"
  "scripts/gen_toc.py --verify-anchors"
  "scripts/check_em_dash.py --selftest"
  "scripts/check_em_dash.py --base $base"
  "scripts/docs_check.py"
  "scripts/check_doc_style.py"
  "scripts/check_doc_style.py --selftest"
  "scripts/check_doc_paths.py"
  "scripts/check_archive.py"
  "scripts/check_archive.py --selftest"
  "scripts/check_feature_status.py --self-test"
  "docs/traceability/gen_module_matrix.py --check"
  "scripts/check_hygiene.py --check"
  "scripts/check_hygiene.py --selftest"
  "scripts/check_todo_ownership.py"
  "scripts/check_todo_ownership.py --selftest"
  "scripts/measure_test_evidence.py --check"
  "scripts/measure_test_evidence.py --selftest"
  "scripts/check_py_idiom.py"
  "scripts/check_py_idiom.py --selftest"
  "scripts/ci_events.py --check"
  "scripts/ci_events.py --selftest"
)
fail=0
for cmd in "${cmds[@]}"; do
  # shellcheck disable=SC2086
  out=$("$py" $cmd 2>&1); rc=$?
  [ "$rc" -eq 0 ] || fail=1
  printf '[rc=%s] %s :: %s\n' "$rc" "$cmd" "$(printf '%s\n' "$out" | grep -v '^\s*$' | tail -1)"
done
exit "$fail"
