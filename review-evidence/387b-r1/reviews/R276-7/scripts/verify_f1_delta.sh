#!/bin/sh
# R276-7: verify the round-4 delta closes R276-6 F1 at a given head.
# Usage: verify_f1_delta.sh <clone> [prev_head] [head]
set -eu
C=${1:?clone}; PREV=${2:-0f003fab3303858ba4db955ad3c0512e67a8018b}
HEAD=${3:-00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b}
cd "$C"
echo "== delta files $PREV..$HEAD"
git diff --raw "$PREV" "$HEAD"
echo "== delta"
git diff "$PREV" "$HEAD"
echo "== every '2700' in tracked text at $HEAD (all paths)"
git grep -n -I -E '2700|2,700' "$HEAD" || true
echo "== current statements of the milan_dp deadline at $HEAD"
git grep -n -I -E 'milan_dp[^_].{0,80}(budget|deadline|seconds)|SUITE_TIMEOUT:-3600|suite_timeout = ' "$HEAD" -- '*.md' '*.py' '*.sh' '*.yml' || true
echo "== history and self-test lines intended unchanged"
git diff --quiet "$PREV" "$HEAD" -- docs/testing/CI_WORKFLOWS.md scripts/measure_test_evidence_selftest.py \
  && echo "CI_WORKFLOWS.md and measure_test_evidence_selftest.py unchanged in delta"
git show "$HEAD":docs/testing/CI_WORKFLOWS.md | sed -n '167p;185p'
git show "$HEAD":scripts/measure_test_evidence_selftest.py | sed -n '294p'
echo "== hosted shard timeout"
git show "$HEAD":.github/workflows/rtl.yml | sed -n '147,152p'
