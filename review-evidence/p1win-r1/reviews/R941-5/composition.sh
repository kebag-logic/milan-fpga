#!/usr/bin/env bash
# Composition receipt for a merge-train candidate: reproduce its tree, list the
# files both sides change, and check every changed path took its side's bytes.
# Usage: composition.sh <clone> <candidate> <first-parent> <pr-head> [live-base]
set -u
cd "$1" || exit 2
C=$2; D=$3; P=$4; L=${5:-}
B=$(git merge-base "$D" "$P")
echo "candidate $C tree $(git rev-parse "$C^{tree}")"
echo "parents   $(git log -1 --format=%P "$C")"
echo "merge-base(first-parent, pr-head) $B"
echo "merge-tree(first-parent, pr-head) $(git merge-tree --write-tree "$D" "$P")"
if [ -n "$L" ]; then
  echo "live base $L tree $(git rev-parse "$L^{tree}") first-parent tree $(git rev-parse "$D^{tree}")"
  echo "merge-tree(live base, pr-head) $(git merge-tree --write-tree "$L" "$P")"
fi
echo "--- PR commits ($B..$P)"; git log --format='%h %s' "$B..$P"
echo "--- PR files"; git diff --name-only "$B" "$P"
echo "--- predecessor files ($B..$D)"; git diff --name-only "$B" "$D"
echo "--- files changed by both"
comm -12 <(git diff --name-only "$B" "$P" | sort) <(git diff --name-only "$B" "$D" | sort)
echo "--- per-path byte check (candidate blob == the changing side's blob; both-sided paths listed)"
for f in $(git diff --name-only "$B" "$P"); do
  [ "$(git rev-parse "$P:$f" 2>/dev/null)" = "$(git rev-parse "$C:$f" 2>/dev/null)" ] || echo "PR path not PR bytes: $f"
done
for f in $(git diff --name-only "$B" "$D"); do
  [ "$(git rev-parse "$D:$f" 2>/dev/null)" = "$(git rev-parse "$C:$f" 2>/dev/null)" ] || echo "predecessor path not predecessor bytes: $f"
done
echo "--- both-sided paths: candidate vs each side"
for f in $(comm -12 <(git diff --name-only "$B" "$P" | sort) <(git diff --name-only "$B" "$D" | sort)); do
  echo "## $f: candidate vs first parent"; git --no-pager diff --no-color -U0 "$D" "$C" -- "$f" | grep '^@@'
  echo "## $f: candidate vs pr-head"; git --no-pager diff --no-color -U0 "$P" "$C" -- "$f" | grep '^@@'
done
