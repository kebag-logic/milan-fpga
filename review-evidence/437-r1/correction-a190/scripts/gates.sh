#!/usr/bin/env bash
# gates.sh: the focused gates at the lane's HEAD, one receipt each, run in sequence.
set -uo pipefail
R=$REVIEWS/437-a190-packet/scripts/rec.sh
MB=$(git -C $LANES/437-container-paragraph-scopes merge-base origin/dev HEAD)
$R toc-selftest python3 -B scripts/gen_toc.py --selftest
$R toc-check python3 -B scripts/gen_toc.py --check
$R toc-anchors python3 -B scripts/gen_toc.py --verify-anchors
$R toc-sites python3 -B scripts/gen_toc.py --sites
$R emdash-selftest python3 -B scripts/check_em_dash.py --selftest
$R emdash-base-mergebase python3 -B scripts/check_em_dash.py --base "$MB"
$R emdash-base-483a133e python3 -B scripts/check_em_dash.py --base 483a133ed08867ea0d300d2b4a027b5b48a4282f
$R emdash-base-88e9276b python3 -B scripts/check_em_dash.py --base 88e9276b2a220c716f64a843f7e1eb8f9265e896
$R docs-check python3 -B scripts/docs_check.py
$R docs-check-selftest python3 -B scripts/docs_check.py --selftest
$R doc-style python3 -B scripts/check_doc_style.py
$R doc-style-selftest python3 -B scripts/check_doc_style.py --selftest
$R doc-paths python3 -B scripts/check_doc_paths.py
$R py-idiom python3 -B scripts/check_py_idiom.py
$R py-idiom-selftest python3 -B scripts/check_py_idiom.py --selftest
$R hygiene python3 -B scripts/check_hygiene.py --check
$R hygiene-selftest python3 -B scripts/check_hygiene.py --selftest
$R naming python3 -B scripts/measure_naming.py --check
$R fail-fast python3 -B scripts/measure_fail_fast.py --check
$R test-evidence python3 -B scripts/measure_test_evidence.py --check
$R cohesion-selftest python3 -B scripts/measure_cohesion.py --selftest
$R control-flow-selftest python3 -B scripts/measure_control_flow.py --selftest
$R todo-ownership python3 -B scripts/check_todo_ownership.py
$R feature-status python3 -B scripts/check_feature_status.py
$R diff-check-branch git diff --check "$MB" HEAD
$R diff-check-worktree git diff --check
$R status git status --porcelain=v1 --untracked-files=all
