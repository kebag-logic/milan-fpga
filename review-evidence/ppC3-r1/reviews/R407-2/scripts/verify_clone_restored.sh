#!/usr/bin/env bash
# Verify the review clone equals the exact head: HEAD, tree, index tree, every tracked
# file's bytes and mode against its blob, no tracked/untracked/ignored drift, no gitlinks.
set -u
C="${1:-$REVIEWS/r407-2-ppC3}"; H=20ec92b7b190d03c46e40be89d236bc9a0702a59; T=a3d4eb5a6e6b8bf770b683d9ab5bd71a916dab6d
cd "$C" || exit 2
rc=0
[ "$(git rev-parse HEAD)" = "$H" ] && echo "HEAD ok $H" || { echo "HEAD MISMATCH"; rc=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$T" ] && echo "tree ok $T" || { echo "TREE MISMATCH"; rc=1; }
[ "$(git write-tree)" = "$T" ] && echo "index tree ok" || { echo "INDEX MISMATCH"; rc=1; }
n=0; bad=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; sha=${rest#* }
  n=$((n+1))
  case "$mode" in
    160000) echo "gitlink $path"; continue;;
    120000) [ "$(printf %s "$(readlink "$path")" | git hash-object --stdin)" = "$sha" ] || { echo "LINK DRIFT $path"; bad=$((bad+1)); } ; continue;;
  esac
  [ "$(git hash-object --no-filters "$path")" = "$sha" ] || { echo "BYTE DRIFT $path"; bad=$((bad+1)); }
  x=$([ -x "$path" ] && echo 100755 || echo 100644)
  [ "$x" = "$mode" ] || { echo "MODE DRIFT $path $x vs $mode"; bad=$((bad+1)); }
done < <(git ls-tree -r "$H")
echo "tracked files checked: $n, drift: $bad"; [ "$bad" = 0 ] || rc=1
echo "gitlinks in head tree: $(git ls-tree -r "$H" | awk '$1=="160000"' | wc -l) (none required: no .gitmodules)"
s=$(git status --porcelain --ignored | wc -l); echo "status entries (tracked, untracked, ignored): $s"; [ "$s" = 0 ] || rc=1
echo "rc=$rc"; exit $rc
