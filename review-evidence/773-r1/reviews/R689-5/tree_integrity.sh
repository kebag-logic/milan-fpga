#!/usr/bin/env bash
# Usage: tree_integrity.sh <clone> <expected-head>
# Checks HEAD, index tree, tracked worktree bytes and modes, initialized gitlinks,
# and that no untracked or ignored entry remains.
set -u
cd "$1" || exit 2
want=$2 rc=0
TMPDIR_GL=$(mktemp)
head=$(git rev-parse HEAD); echo "HEAD $head"; [ "$head" = "$want" ] || rc=1
it=$(git write-tree); ht=$(git rev-parse HEAD^{tree}); echo "index-tree $it head-tree $ht"; [ "$it" = "$ht" ] || rc=1
git diff --quiet && git diff --cached --quiet && echo "no tracked diff" || { echo "TRACKED DIFF"; git diff --stat; rc=1; }
blobs=0 bad=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1 type=$2 sha=$3
  [ "$type" = blob ] || continue
  blobs=$((blobs+1))
  if [ "$mode" = 120000 ]; then got=$(readlink -- "$path" | tr -d '\n' | git hash-object --stdin)
  else got=$(git hash-object --no-filters -- "$path"); fi
  fm=100644; [ -L "$path" ] && fm=120000; [ ! -L "$path" ] && [ -x "$path" ] && fm=100755
  if [ "$got" != "$sha" ] || [ "$fm" != "$mode" ]; then echo "MISMATCH $mode $sha $path got $fm $got"; bad=$((bad+1)); fi
done < <(git ls-tree -r --full-tree HEAD)
echo "blobs $blobs mismatches $bad"; [ $bad -eq 0 ] || rc=1
git ls-tree -r HEAD | awk '$2=="commit"{print $3, $4}' | while read -r sha path; do
  if [ -e "$path/.git" ]; then got=$(git -C "$path" rev-parse HEAD); [ "$got" = "$sha" ] && echo "gitlink ok $path" || echo "GITLINK MISMATCH $path $got != $sha"
  else echo "gitlink uninitialized $path"; fi
done > "$TMPDIR_GL" ; cat "$TMPDIR_GL"; grep -q MISMATCH "$TMPDIR_GL" && rc=1
n=$(git status --porcelain --ignored | wc -l); echo "untracked+ignored entries $n"; [ "$n" -eq 0 ] || { git status --porcelain --ignored | head; rc=1; }
echo "rc $rc"; exit $rc
