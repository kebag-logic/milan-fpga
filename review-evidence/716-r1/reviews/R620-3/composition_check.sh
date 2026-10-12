#!/usr/bin/env bash
# Composition identity checks for the issue 716 merge-train candidate.
# Usage: composition_check.sh <clone>
# Prints each check and exits nonzero on the first failed expectation.
set -euo pipefail
cd "$1"
cand=194b7c4114c609fa3dc3b10f82292a45e7781b0e
dev=c6bd08c6f52632c6d33d834ce842ac3cf63f29cc
pr=941e15593ef3dbf561bd8ed75aaf680f5d146a41
pr_base=09c7231eca343607c97c0d66abebb2553688712c
fail() { echo "FAIL: $*"; exit 1; }

echo "== 1. candidate identity"
[ "$(git rev-parse $cand^1)" = $dev ] || fail "first parent is not dev"
[ "$(git rev-parse $cand^2)" = $pr ] || fail "second parent is not the PR head"
[ "$(git merge-base $dev $pr)" = $pr_base ] || fail "merge base is not $pr_base"
tree=$(git rev-parse "$cand^{tree}")
auto=$(git merge-tree --write-tree $dev $pr | head -n 1)
echo "candidate tree $tree; mechanical clean merge tree $auto"
[ "$tree" = "$auto" ] || fail "candidate tree differs from the clean automatic merge"

echo "== 2. files changed on both sides since the merge base"
git diff --name-only $pr_base $dev | sort > /tmp/r620-3-dev.$$
git diff --name-only $pr_base $pr | sort > /tmp/r620-3-pr.$$
both=$(comm -12 /tmp/r620-3-dev.$$ /tmp/r620-3-pr.$$)
echo "dev side: $(wc -l < /tmp/r620-3-dev.$$) files; PR side: $(wc -l < /tmp/r620-3-pr.$$) files"
echo "both: $both"
[ "$both" = docs/testing/CI_WORKFLOWS.md ] || fail "unexpected overlap"

echo "== 3. PR-only files are byte-identical to the PR head in the candidate"
for f in $(comm -13 /tmp/r620-3-dev.$$ /tmp/r620-3-pr.$$); do
  a=$(git rev-parse "$cand:$f"); b=$(git rev-parse "$pr:$f")
  echo "$f cand=$a pr=$b"; [ "$a" = "$b" ] || fail "$f differs"
done
echo "== 4. dev-only files are byte-identical to dev in the candidate"
n=0
for f in $(comm -23 /tmp/r620-3-dev.$$ /tmp/r620-3-pr.$$); do
  a=$(git ls-tree $cand -- "$f" | awk '{print $1,$3}')
  b=$(git ls-tree $dev -- "$f" | awk '{print $1,$3}')
  [ "$a" = "$b" ] || fail "$f differs"; n=$((n+1))
done
echo "$n dev-only paths (mode and object) identical"

echo "== 5. the shared page carries each side's hunks byte-identically"
P=docs/testing/CI_WORKFLOWS.md
h() { git diff "$1" "$2" -- $P | grep '^[+-]' | grep -v '^[+-][+-]'; }
cmp <(h $pr $cand) <(h $pr_base $dev) || fail "dev hunk altered"
cmp <(h $dev $cand) <(h $pr_base $pr) || fail "PR hunks altered"
echo "dev hunk: $(h $pr_base $dev | wc -l) changed lines; PR hunks: $(h $pr_base $pr | wc -l) changed lines; both carried exactly"
git diff -U0 $pr_base $dev -- $P | grep '^@@'
git diff -U0 $pr_base $pr -- $P | grep '^@@'

echo "== 6. dev-side paths named by the PR's CI and firmware inputs"
while read -r f; do
  git grep -n -F -e "$f" $cand -- sw/firmware .github/workflows/rtl-fast.yml \
    scripts/ci_events.py scripts/ci_scope.py scripts/ci_rv32_sdk.py || true
done < /tmp/r620-3-dev.$$
rm -f /tmp/r620-3-dev.$$ /tmp/r620-3-pr.$$
echo "COMPOSITION CHECK: PASS"
