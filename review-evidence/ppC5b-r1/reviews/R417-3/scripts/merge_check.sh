#!/usr/bin/env bash
# Re-performs the merge of main 3f3ea56b into lane 2acd4025 in a disposable worktree and
# compares every path with the published merge a8fe574 and the final head 441d646.
# usage: merge_check.sh <repo> <scratch-dir>
set -euo pipefail
REPO=$1; WT=$2/remerge
LANE=2acd4025782bff4aabbae73252476be34ea8b00d MAIN=3f3ea56ba61829718a6a288600ab4fdac73aa5ba
MERGE=a8fe57448bbaa8dabc7e842600aa4f10e04336e3 BASE=$(git -C "$REPO" merge-base $LANE $MAIN)
echo "base=$BASE"
echo "merge parents: $(git -C "$REPO" rev-parse $MERGE^1 $MERGE^2 | tr '\n' ' ')"
rm -rf "$WT"; git -C "$REPO" worktree add -q --detach "$WT" $LANE
cd "$WT"
git -c user.name=x -c user.email=x@x merge --no-commit --no-ff $MAIN >/dev/null 2>&1 || true
echo "== conflicted paths in an independent re-merge:"; git diff --name-only --diff-filter=U
echo "== classification of every path either side touched:"
comm -12 <(git -C "$REPO" diff --name-only $BASE $LANE | sort) <(git -C "$REPO" diff --name-only $BASE $MAIN | sort) > /tmp/both.$$
for f in $(git -C "$REPO" diff --name-only $BASE $MAIN); do
  m=$(git -C "$REPO" rev-parse -q --verify $MAIN:$f || echo none); r=$(git -C "$REPO" rev-parse -q --verify $MERGE:$f || echo none)
  if grep -qx "$f" /tmp/both.$$; then echo "BOTH      $f"; elif [ "$m" = "$r" ]; then echo "MAIN-ONLY $f merge==main"; else echo "MAIN-ONLY $f MERGE DIFFERS FROM MAIN"; fi
done
nl=0; bad=0
for f in $(git -C "$REPO" diff --name-only $BASE $LANE); do
  grep -qx "$f" /tmp/both.$$ && continue; nl=$((nl+1))
  [ "$(git -C "$REPO" rev-parse -q --verify $LANE:$f || echo none)" = "$(git -C "$REPO" rev-parse -q --verify $MERGE:$f || echo none)" ] || { echo "LANE-ONLY $f MERGE DIFFERS FROM LANE"; bad=$((bad+1)); }
done
echo "lane-only paths: $nl, differing from lane: $bad"
echo "== paths changed by the merge relative to neither parent's version (non-both):"
git -C "$REPO" diff --name-only $LANE $MERGE | while read f; do grep -qx "$f" /tmp/both.$$ && continue; [ "$(git -C "$REPO" rev-parse -q --verify $MAIN:$f||echo n)" = "$(git -C "$REPO" rev-parse -q --verify $MERGE:$f||echo n)" ] || echo "UNEXPECTED $f"; done
echo "== both-touched: lines added by each side (vs base) missing from merge"
for f in $(cat /tmp/both.$$); do
  for side in LANE MAIN; do s=${!side}
    git -C "$REPO" diff -U0 $BASE $s -- "$f" | grep '^+' | grep -v '^+++' | sed 's/^+//' | sort > /tmp/add.$$
    git -C "$REPO" show $MERGE:"$f" | sort > /tmp/m.$$
    miss=$(comm -23 <(sort -u /tmp/add.$$) <(sort -u /tmp/m.$$) | wc -l)
    echo "$f side=$side added_lines=$(wc -l </tmp/add.$$) missing_in_merge=$miss"
    comm -23 <(sort -u /tmp/add.$$) <(sort -u /tmp/m.$$) | sed 's/^/    MISSING: /'
  done
  # lines in merge in neither parent
  extra=$(comm -23 <(git -C "$REPO" show $MERGE:"$f" | sort -u) <(cat <(git -C "$REPO" show $LANE:"$f") <(git -C "$REPO" show $MAIN:"$f") | sort -u))
  echo "$f lines in merge in neither parent: $(printf '%s' "$extra" | grep -c . || true)"; printf '%s\n' "$extra" | grep . | sed 's/^/    NEW: /' || true
done
echo "== merge auto-result vs published merge for non-conflicted paths:"
for f in $(git diff --name-only HEAD; git diff --cached --name-only) ; do :; done
git diff --cached --name-only --diff-filter=AM | sort -u | while read f; do
  [ "$(git hash-object "$f")" = "$(git -C "$REPO" rev-parse $MERGE:$f)" ] && echo "same $f" || echo "DIFF $f"; done
git merge --abort || true; cd /; git -C "$REPO" worktree remove --force "$WT"; rm -f /tmp/both.$$ /tmp/add.$$ /tmp/m.$$
