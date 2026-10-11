#!/usr/bin/env bash
# Composition receipt: the candidate merge commit equals a clean 3-way merge of
# dev parent and PR head, and every line either side added (or removed) in the
# shared files survives (or stays removed) in the candidate.
# usage: composition_check.sh <checkout> <base> <dev> <pr> <candidate> <tmpdir> <file>...
set -u
co=$1; mb=$2; dev=$3; pr=$4; cand=$5; tmp=$6; shift 6
g() { git -C "$co" -c core.commitGraph=false "$@"; }
mkdir -p "$tmp"
echo "## parents of candidate: $(g rev-parse "$cand^1") $(g rev-parse "$cand^2")"
echo "## merge base of dev and PR: $(g merge-base "$dev" "$pr")"
echo "## recomputed merge tree: $(g merge-tree --write-tree "$dev" "$pr" | head -n 1)"
echo "## candidate tree:        $(g rev-parse "$cand^{tree}")"
echo "## files PR changed since base that dev also changed:"
comm -12 <(g diff --name-only "$mb" "$pr" | sort) <(g diff --name-only "$mb" "$dev" | sort)
echo "## files candidate differs from PR head (expect dev's files only):"
g diff --name-only "$pr" "$cand"
echo "## files candidate differs from dev (expect PR's files only):"
g diff --name-only "$dev" "$cand"
for f in "$@"; do
  k=$(echo "$f" | tr '/' '_')
  g show "$mb:$f" >"$tmp/$k.base"; g show "$dev:$f" >"$tmp/$k.dev"
  g show "$pr:$f" >"$tmp/$k.pr"; g show "$cand:$f" >"$tmp/$k.cand"
  cp "$tmp/$k.dev" "$tmp/$k.merged"
  git merge-file "$tmp/$k.merged" "$tmp/$k.base" "$tmp/$k.pr"; mrc=$?
  cmp -s "$tmp/$k.merged" "$tmp/$k.cand"; crc=$?
  add() { diff "$tmp/$k.base" "$tmp/$k.$1" | sed -n 's/^> //p' | sort -u; }
  del() { diff "$tmp/$k.base" "$tmp/$k.$1" | sed -n 's/^< //p' | sort -u; }
  cs=$(sort -u "$tmp/$k.cand")
  echo "-- $f"
  echo "   merge-file conflicts=$mrc ; merged == candidate: $([ $crc = 0 ] && echo yes || echo NO)"
  echo "   dev-added lines missing from candidate: $(comm -23 <(add dev) <(echo "$cs") | wc -l) of $(add dev | wc -l)"
  echo "   PR-added lines missing from candidate:  $(comm -23 <(add pr) <(echo "$cs") | wc -l) of $(add pr | wc -l)"
  echo "   dev-removed lines still in candidate:   $(comm -12 <(del dev) <(echo "$cs") | wc -l) of $(del dev | wc -l)"
  echo "   PR-removed lines still in candidate:    $(comm -12 <(del pr) <(echo "$cs") | wc -l) of $(del pr | wc -l)"
done
