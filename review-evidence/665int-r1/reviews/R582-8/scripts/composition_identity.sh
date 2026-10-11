#!/usr/bin/env bash
# composition_identity.sh <clone> : prove the candidate merge commit is the
# conflict-free automatic merge of its two parents, and that each side's
# change lines survive byte for byte, per overlapping file and in total.
set -euo pipefail
cd "$1"
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.commitGraph GIT_CONFIG_VALUE_0=false
G=/usr/bin/git
CAND=e52d7525ae0c5c9ac669843432187ddcd9071686
PRED=eb86b843557c6d9300847e3b6e12851604580b69   # first parent: dev cfadd767 + 696
SRC=67c1285b3b28b12a3af4f3f3aae6e92befd5febb    # second parent: PR #704 source head
[ "$($G rev-parse "$CAND^1")" = "$PRED" ] && [ "$($G rev-parse "$CAND^2")" = "$SRC" ]
MB=$($G merge-base "$PRED" "$SRC")
echo "candidate $CAND tree $($G rev-parse "$CAND^{tree}")"
echo "parents   $PRED (pred) $SRC (source); merge base $MB"
auto=$($G merge-tree --write-tree "$PRED" "$SRC")
echo "automatic merge tree $auto ($( [ "$auto" = "$($G rev-parse "$CAND^{tree}")" ] && echo EQUAL || echo DIFFERENT ) to the candidate's)"
h() { $G diff --no-ext-diff --no-textconv --no-renames "$@" | grep '^[-+]' | grep -v -e '^+++ ' -e '^--- ' | sha256sum | cut -c1-16; }
echo "PR change lines:   source $(h "$MB" "$SRC")  candidate $(h "$PRED" "$CAND")"
echo "pred change lines: pred   $(h "$MB" "$PRED")  candidate $(h "$SRC" "$CAND")"
$G diff --name-only "$MB" "$SRC" | sort > /tmp/ci_pr.$$
$G diff --name-only "$MB" "$PRED" | sort > /tmp/ci_pred.$$
echo "files: PR $(wc -l < /tmp/ci_pr.$$), predecessors $(wc -l < /tmp/ci_pred.$$), both:"
comm -12 /tmp/ci_pr.$$ /tmp/ci_pred.$$ | while read -r f; do
  echo "  $f  PR $(h "$MB" "$SRC" -- "$f")=$(h "$PRED" "$CAND" -- "$f")  pred $(h "$MB" "$PRED" -- "$f")=$(h "$SRC" "$CAND" -- "$f")"
done
rm -f /tmp/ci_pr.$$ /tmp/ci_pred.$$
echo "first-parent history:"; $G log --format='  %h %s' --first-parent -5 "$CAND" | cut -c1-120
echo "gitlinks:"; $G ls-tree "$CAND" external gptp-processor protocol-processor third_party/lwSRP third_party/verilog-axis | sed 's/^/  /'
