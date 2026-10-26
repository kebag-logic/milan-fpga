#!/usr/bin/env bash
# Run the offline gates for PR #785 at the reviewed head, concurrently, one log and rc per gate.
# Usage: run_gates.sh <checkout> <receipt-dir>
set -u
repo=$1; out=$2; mkdir -p "$out"
cd "$repo" || exit 2
install_dir=$(mktemp -d)
install -m 0555 scripts/act_ci.py "$install_dir/act_ci.py"
sha256sum "$install_dir/act_ci.py" | sed "s#$install_dir/##" > "$out/installed-act_ci.sha256"
run() { name=$1; shift; ( "$@" > "$out/$name.log" 2>&1; echo $? > "$out/$name.rc" ) & }
run act-ci-selftest python3 scripts/act_ci.py --selftest
run act-ci-contract-gate python3 -I "$install_dir/act_ci.py" --selftest --worktree "$repo"
run ci-events-check python3 scripts/ci_events.py --check
run ci-events-selftest python3 scripts/ci_events.py --selftest
run docs-check python3 scripts/docs_check.py
run em-dash python3 scripts/check_em_dash.py --base d385b38e5282b395ca55d49d135e46a93f56a340
run gen-toc-check python3 scripts/gen_toc.py --check
run doc-paths python3 scripts/check_doc_paths.py
run baremetal-check python3 scripts/check_baremetal_only.py --check
run doc-style python3 scripts/check_doc_style.py
run feature-status python3 scripts/check_feature_status.py
run py-idiom python3 scripts/check_py_idiom.py
run hygiene python3 scripts/check_hygiene.py
run todo-ownership python3 scripts/check_todo_ownership.py
run evidence-pins python3 scripts/generate_ci_evidence_pins.py --check
run runtime-evidence-selftest python3 scripts/ci_runtime_evidence_selftest.py
run gate-workflows-check python3 scripts/ci_gate_workflows.py --check
run github-diff git diff --exit-code d385b38e5282b395ca55d49d135e46a93f56a340 -- .github
wait
rm -rf "$install_dir"
for f in "$out"/*.rc; do printf '%s %s\n' "$(cat "$f")" "$(basename "$f" .rc)"; done
