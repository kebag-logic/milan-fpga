#!/usr/bin/env bash
# Replays the delta checks of R731-5 in any clone that has the named commits.
# Usage: scripts_replay.sh <clone-dir>
set -u
cd "$1"
H=86a349d5399d8abc40b819d09806fc8245682609; OLD=cbc7c6043ebf84d5bcd74652dc0a7131b7d54271; D=8adf5c990bad73e80852e9c1df95163792a0deb2
echo "trees: $(git rev-parse $OLD^{tree}) $(git rev-parse $H^{tree})"
echo "parents: $(git log -1 --format=%P $H)"
echo "message lines: $(git log -1 --format=%B $H | sed '/^$/d' | wc -l)"
for X in $OLD $H; do
  base="$(git merge-base --all $D $X)"
  echo "== $X bases=$(echo "$base" | wc -l)"
  git cat-file -e "$base^{commit}" 2>/dev/null; echo "classifier cat-file rc=$?"
  m=$(git merge-tree --write-tree $D $X); echo "merged=$m files=$(git diff --no-renames --name-only $D $m | wc -l)"
done
echo "dev merge honest: $(git merge-tree --write-tree $D^1 $D^2) vs $(git rev-parse $D^{tree})"
