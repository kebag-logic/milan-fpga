#!/bin/sh
# Reviewer probe: redo round 4's merge and compare it with the committed one.
# Usage: remerge_check.sh <clone-with-both-parents> <scratch-dir>
# Clones the repository into the scratch dir, merges dev 1269cdaf into lane
# 0b066b6e with --no-ff, then reports, per path the committed merge c1288648
# changed against the lane parent: whether the automatic result equals the
# committed blob, and how each side's delta is carried in the two auto-merged
# files and the two conflicted changelog sections.
set -u
SRC=$1
WORK=$2/remerge
LANE=0b066b6e66df2a3ba3167805a6a591f8b96fa449
DEV=1269cdafb4bb964c757baae0f0c5a932d43f540b
BASE=cdf49d1a28527562888f0a903de51b6b15b1244f
MERGE=c12886486c1e4acf2003bfaba25db2a307446428
rm -rf "$WORK"
git clone -q --no-checkout "$SRC" "$WORK" || exit 2
cd "$WORK" || exit 2
git -c advice.detachedHead=false checkout -q "$LANE" || exit 2
echo "parents of $MERGE: $(git rev-parse "$MERGE^1") $(git rev-parse "$MERGE^2")"
echo "merge-base lane/dev: $(git merge-base "$LANE" "$DEV")"
git -c user.name=r -c user.email=r@invalid merge --no-ff --no-edit "$DEV" >/dev/null 2>&1
echo "conflicted paths:"; git diff --name-only --diff-filter=U | sed 's/^/  /'
echo "auto-merged paths vs the committed merge:"
for f in $(git diff --cached --name-only --diff-filter=M HEAD); do
  a=$(git rev-parse ":0:$f"); b=$(git rev-parse "$MERGE:$f")
  [ "$a" = "$b" ] && echo "  SAME $f" || echo "  DIFF $f (auto $a, committed $b)"
done
echo "port_docs.budget, auto-merged vs committed:"
git diff --no-ext-diff ":0:scripts/port_docs.budget" "$MERGE:scripts/port_docs.budget" | grep '^[-+][^-+]' | sed 's/^/  /'
echo "naming.budget, committed merge vs lane parent: $(git diff --no-ext-diff --quiet "$LANE" "$MERGE" -- scripts/naming.budget && echo identical || echo differs)"
for f in docs/reference/REGISTER_MAP.md scripts/measure_test_evidence.py; do
  git diff --no-ext-diff "$BASE" "$DEV" -- "$f" | grep '^[-+][^-+]' | sort > /tmp/r432.dev.$$
  git diff --no-ext-diff "$LANE" "$MERGE" -- "$f" | grep '^[-+][^-+]' | sort > /tmp/r432.mgl.$$
  git diff --no-ext-diff "$BASE" "$LANE" -- "$f" | grep '^[-+][^-+]' | sort > /tmp/r432.lane.$$
  git diff --no-ext-diff "$DEV" "$MERGE" -- "$f" | grep '^[-+][^-+]' | sort > /tmp/r432.mgd.$$
  d=$(cmp -s /tmp/r432.dev.$$ /tmp/r432.mgl.$$ && echo yes || echo NO)
  l=$(cmp -s /tmp/r432.lane.$$ /tmp/r432.mgd.$$ && echo yes || echo NO)
  echo "$f: dev delta carried $d; lane delta carried $l"
  rm -f /tmp/r432.*.$$
done
sec() { git show "$1:CHANGELOG.md" | awk -v h="$2" '$0==h{p=1;print;next} p&&/^## /{exit} p{print}' | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}' | sha256sum | cut -c1-16; }
for h in "## Unreleased - AAF or CRF media-clock following" "## Unreleased - processor pin 631eeb34"; do
  echo "CHANGELOG \"$h\": lane $(sec $LANE "$h") dev $(sec $DEV "$h") merge $(sec $MERGE "$h")"
done
echo "design page header at the merge:"; git show "$MERGE:docs/design/MEDIA_CLOCK_FOLLOWING.md" | sed -n 6,12p | sed 's/^/  /'
