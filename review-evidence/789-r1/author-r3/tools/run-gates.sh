#!/usr/bin/env bash
# Run every gate the #789 round-3 change touches, concurrently, one log and one
# rc file per gate. The python3 first on PATH is the interpreter under test.
# Usage: run-gates.sh <worktree> <receipts-dir> <md-python>
set -u
tree="$1"
out="$2"
md="$3"
mkdir -p "$out"
cd "$tree" || exit 2

gate() {
  local label="$1"
  shift
  ( "$@" > "$out/$label.log" 2>&1; echo $? > "$out/$label.rc" ) &
}

runner() {
  python3 scripts/act_ci.py --selftest || return $?
  local install_dir
  install_dir="$(mktemp -d)"
  install -m 0555 scripts/act_ci.py "$install_dir/act_ci.py"
  python3 -I "$install_dir/act_ci.py" --selftest --worktree "$PWD"
  local rc=$?
  rm -rf "$install_dir"
  return "$rc"
}

base=76de691e5625cc4ea2f9a19def9e07c1183a14ee
{ python3 --version; python3 -c 'import yaml; print("PyYAML", yaml.__version__)'; git rev-parse HEAD; git status --short; } \
  > "$out/environment.txt" 2>&1
gate ci_gate_workflows-check python3 scripts/ci_gate_workflows.py --check
gate ci_gate_workflows_selftest python3 scripts/ci_gate_workflows_selftest.py
for s in ci_case_receipts ci_make_cases ci_maap_cases ci_capture_cases ci_suite_pieces ci_suite_collect \
         ci_fail_fast ci_runtime_evidence ci_install_cache ci_workflow_plan ci_manifest; do
  gate "${s}_selftest" python3 "scripts/${s}_selftest.py"
done
gate generate_ci_evidence_pins-check python3 scripts/generate_ci_evidence_pins.py --check
gate ci_scope-selftest python3 scripts/ci_scope.py --selftest
gate ci_events-check python3 scripts/ci_events.py --check
gate ci_events-selftest python3 scripts/ci_events.py --selftest
gate act_ci-runner-contract runner
gate check_py_idiom python3 scripts/check_py_idiom.py
gate check_py_idiom-selftest python3 scripts/check_py_idiom.py --selftest
gate check_baremetal_only-check python3 scripts/check_baremetal_only.py --check
gate check_hygiene-check python3 scripts/check_hygiene.py --check
gate check_todo_ownership python3 scripts/check_todo_ownership.py
gate measure_naming-check python3 scripts/measure_naming.py --check
gate measure_test_evidence-check python3 scripts/measure_test_evidence.py --check
gate measure_fail_fast-check python3 scripts/measure_fail_fast.py --check
gate docs_check "$md" scripts/docs_check.py
gate check_em_dash "$md" scripts/check_em_dash.py --base "$base"
gate check_doc_style "$md" scripts/check_doc_style.py
gate gen_toc-check "$md" scripts/gen_toc.py --check
gate gen_toc-verify-anchors "$md" scripts/gen_toc.py --verify-anchors
gate check_doc_paths "$md" scripts/check_doc_paths.py
wait
fail=0
for rc in "$out"/*.rc; do
  printf '%s %s\n' "$(cat "$rc")" "$(basename "$rc" .rc)"
  [ "$(cat "$rc")" = 0 ] || fail=1
done
exit "$fail"
