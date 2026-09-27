#!/bin/bash
# Item 1: ci_scope selftest and classification at the head, run on the clone.
# Usage: 10_ci_scope.sh <clone>
set -u
C=${1:?clone}; cd "$C" || exit 2
export PYTHONDONTWRITEBYTECODE=1
echo "--- head $(git rev-parse HEAD)"
out=$(python3 scripts/ci_scope.py --selftest 2>&1); echo "head selftest rc=$?"
grep -E "FAIL|PASS|selftest" <<<"$out" | tail -5
echo "--- classify PR files base..head"
git diff --no-renames --name-only 9e9954e96bf55181edb9949ae94c9abd4ab6aaf5 HEAD | python3 scripts/ci_scope.py; echo "rc=$?"
echo "--- docs-only edit to the gate-read page"
echo docs/AAF_LATENCY_TAPS.md | python3 scripts/ci_scope.py; echo "rc=$?"
echo "--- a plain docs page control"
echo docs/README.md | python3 scripts/ci_scope.py; echo "rc=$?"
echo "--- GATE_READ_DOCS"
python3 -c "import sys; sys.path.insert(0,'scripts'); import ci_scope as c; print(c.GATE_READ_DOCS)"
