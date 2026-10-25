#!/bin/sh
# Re-derive the merge composition of PR #778's round-3 delta from git objects only.
# Usage: sh compose_check.sh <repo>   (any clone holding 01fc5475, ae255ead and f8775f7b)
set -eu
cd "$1"
B=01fc54756f1ffb0a3aa836681215e8321ee7e86c D=ae255ead86d59277762444c44bb3086ab1879448 H=f8775f7b92b1ceff106ebb02b0e2f4ca48972ad7
echo "parents of H: $(git rev-parse $H^1 $H^2 | tr '\n' ' ')"
MB=$(git merge-base $B $D); echo "merge base: $MB"
T=$(git merge-tree --write-tree --name-only $B $D | head -1 || true)
echo "auto-merge tree: $T (conflicts listed by merge-tree above)"
echo "files differing between auto-merge and recorded tree:"; git diff --name-only $T $H^{tree}
for f in hdl/ieee1722/crf/KL_crf_tx.sv hdl/milan/milan_datapath.sv docs/testing/TESTING.md docs/reference/MILAN_COMPLIANCE_MATRIX.md; do
  a=$(git diff -U0 $MB $B -- $f | grep '^[+-][^+-]' | sha256sum | cut -c1-16); b=$(git diff -U0 $D $H -- $f | grep '^[+-][^+-]' | sha256sum | cut -c1-16)
  c=$(git diff -U0 $MB $D -- $f | grep '^[+-][^+-]' | sha256sum | cut -c1-16); d=$(git diff -U0 $B $H -- $f | grep '^[+-][^+-]' | sha256sum | cut -c1-16)
  echo "$f branch-side $a vs D..H $b $( [ $a = $b ] && echo same || echo DIFF ); dev-side $c vs B..H $d $( [ $c = $d ] && echo same || echo DIFF )"
done
for s in "per-source TSpec:$B" "talker capture-to-wire latency:$D"; do t=${s%%:*}; r=${s##*:}
  x=$(git show $r:CHANGELOG.md | awk -v t="## Unreleased - $t" '$0==t{f=1;print;next} f&&/^## /{exit} f' | sha256sum | cut -c1-16)
  y=$(git show $H:CHANGELOG.md | awk -v t="## Unreleased - $t" '$0==t{f=1;print;next} f&&/^## /{exit} f' | sha256sum | cut -c1-16)
  echo "CHANGELOG '$t': side $x head $y $( [ $x = $y ] && echo same || echo DIFF )"; done
echo "CHANGELOG lines: base $(git show $MB:CHANGELOG.md | wc -l) branch $(git show $B:CHANGELOG.md | wc -l) dev $(git show $D:CHANGELOG.md | wc -l) head $(git show $H:CHANGELOG.md | wc -l)"
