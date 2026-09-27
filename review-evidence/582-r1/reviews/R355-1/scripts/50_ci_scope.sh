#!/bin/bash
# Run scripts/ci_scope.py --selftest at the exact head and at the source base,
# in disposable git worktree-free exports that keep the tracked file list.
# Usage: 50_ci_scope.sh <clone>
set -u
C=${1:?clone}; cd "$C" || exit 2
echo "--- head $(git rev-parse HEAD)"
python3 scripts/ci_scope.py --selftest > /tmp/r355-ci-scope-head.log 2>&1; echo "head selftest rc=$?"
grep -E "FAIL|FAILURE" /tmp/r355-ci-scope-head.log
echo "--- how ci_scope classifies the PR's changed files (base..head)"
git diff --no-renames --name-only 9e9954e96bf55181edb9949ae94c9abd4ab6aaf5 HEAD | python3 scripts/ci_scope.py; echo "rc=$?"
echo "--- a docs-only edit to the gate-read page"
echo docs/AAF_LATENCY_TAPS.md | python3 scripts/ci_scope.py; echo "rc=$?"
rm -f /tmp/r355-ci-scope-head.log
