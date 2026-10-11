#!/usr/bin/env bash
# Composition provenance for a merge-train candidate: the candidate tree equals
# a fresh mechanical merge of its parents, the PR's per-file patches are carried
# unchanged, and the files both the PR and dev changed since the lane base are
# listed with the hunk ranges of each side. Read-only.
# usage: composition_check.sh <repo> <candidate> <dev-parent> <pr-head>
set -u
repo=$1 cand=$2 dev=$3 pr=$4
cd "$repo" || exit 2
g() { git "$@" 2>/dev/null; }
mb=$(g merge-base "$dev" "$pr")
echo "candidate $(g rev-parse "$cand") tree $(g rev-parse "$cand^{tree}")"
echo "parents   $(g rev-parse "$cand^1") $(g rev-parse "$cand^2")"
echo "lane base (merge-base dev, pr) $mb"
echo "fresh merge-tree of dev and pr: $(g merge-tree --write-tree "$dev" "$pr" | head -1)"
echo
echo "== per-file patch identity, PR (base..head) against candidate (dev..candidate)"
for f in $(g diff --name-only "$dev" "$cand"); do
  a=$(g diff "$mb" "$pr" -- "$f" | git patch-id --stable | cut -c1-40)
  b=$(g diff "$dev" "$cand" -- "$f" | git patch-id --stable | cut -c1-40)
  [ "$a" = "$b" ] && echo "same  $f" || echo "DIFF  $f"
done
echo
echo "== files changed on both sides since the lane base"
both=$(comm -12 <(g diff --name-only "$mb" "$pr" | sort) <(g diff --name-only "$mb" "$dev" | sort))
for f in $both; do
  echo "-- $f"
  echo "   dev hunks: $(g diff -U0 "$mb" "$dev" -- "$f" | grep '^@@' | sed 's/ @@.*//; s/@@ //' | tr '\n' ' ')"
  echo "   pr  hunks: $(g diff -U0 "$mb" "$pr" -- "$f" | grep '^@@' | sed 's/ @@.*//; s/@@ //' | tr '\n' ' ')"
  echo "   dev commits: $(g log --format=%h --first-parent "$mb..$dev" -- "$f" | tr '\n' ' ')"
done
echo
echo "== dev first-parent merges since the lane base"
g log --oneline --first-parent "$mb..$dev"
echo
echo "== gitlinks at the candidate"
g ls-files -s | awk '$1 == 160000'
