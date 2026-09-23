#!/usr/bin/env bash
# Composition scope of the #504 merge-train candidate, from Git alone.
# Usage: composition_scope.sh <candidate clone>
set -u
cd "$1" || exit 2
export GIT_NO_REPLACE_OBJECTS=1
CAND=50c0d00ac3e7b7aa319ba4eab995d7e12b89149e
BASE=18271bebbd1a4abf2e32e7783477573114e2a5fa
PR=4876423d4cf8e89b820c56f8339f230abefb4827
DEV=ede8d48ecd7c7f589a14b957951f040d92c99c70
echo "candidate parents: $(git rev-parse "$CAND^1") $(git rev-parse "$CAND^2")"
echo "candidate tree:    $(git rev-parse "$CAND^{tree}")"
echo "merge-tree $BASE $PR: $(git merge-tree --write-tree "$BASE" "$PR") (exit $?)"
MB=$(git merge-base "$BASE" "$PR")
echo "merge bases(PR, candidate base): $(git merge-base --all "$BASE" "$PR" | tr '\n' ' ')"
echo "base parents: $(git rev-parse "$BASE^1") (live dev $DEV) $(git rev-parse "$BASE^2")"
echo "== predecessor side $MB..$BASE (files)"
git diff --name-only "$MB" "$BASE" | sort > /tmp/cs_base.$$
cat /tmp/cs_base.$$
echo "== PR side $MB..$PR (files)"
git diff --name-only "$MB" "$PR" | sort > /tmp/cs_pr.$$
cat /tmp/cs_pr.$$
echo "== files changed by BOTH sides"
comm -12 /tmp/cs_base.$$ /tmp/cs_pr.$$
echo "== PR files: blob at candidate vs PR head vs candidate base"
while read -r f; do
  c=$(git rev-parse "$CAND:$f"); p=$(git rev-parse "$PR:$f")
  b=$(git rev-parse -q --verify "$BASE:$f" || echo absent)
  printf '%s cand=%s pr=%s base=%s %s\n' "$f" "${c:0:12}" "${p:0:12}" "${b:0:12}" \
    "$([ "$c" = "$p" ] && echo CAND=PR || echo CAND!=PR)"
done < /tmp/cs_pr.$$
echo "== predecessor files: candidate vs candidate base"
while read -r f; do
  c=$(git rev-parse "$CAND:$f"); b=$(git rev-parse "$BASE:$f")
  printf '%s %s\n' "$f" "$([ "$c" = "$b" ] && echo CAND=BASE || echo CAND!=BASE)"
done < /tmp/cs_base.$$
echo "== sw/builder/test_builder.py history on each side"
echo "predecessor side commits touching it: $(git rev-list --count "$MB..$BASE" -- sw/builder/test_builder.py)"
echo "earlier dev delta merged into the PR lane: $(git log --format='%h %s' 52711029..$MB -- sw/builder/test_builder.py)"
git show 099e191137dd2797407fb8345a452bcc7a965608 -- sw/builder/test_builder.py > /tmp/cs_099.$$
git apply --check --reverse /tmp/cs_099.$$ && echo "099e1911 postimage present verbatim at candidate (reverse-apply check exit 0)"
echo "== RTL/firmware scope touched by either side (hdl sw/firmware sw/litex configs gitlinks)"
git diff --name-only "$MB" "$CAND" -- hdl sw/firmware sw/litex configs | wc -l
git ls-tree "$MB" gptp-processor protocol-processor third_party/verilog-axis external
git ls-tree "$CAND" gptp-processor protocol-processor third_party/verilog-axis external
rm -f /tmp/cs_base.$$ /tmp/cs_pr.$$ /tmp/cs_099.$$
