#!/usr/bin/env bash
# Verify a review clone is byte-exact at an expected head: HEAD, tree, index,
# worktree, every tracked blob's bytes and mode, gitlinks, untracked/ignored files.
# Usage: verify_clone.sh <clone> <head-sha> <tree-sha>
set -u; C=$1; H=$2; T=$3; cd "$C" || exit 2; bad=0
[ "$(git rev-parse HEAD)" = "$H" ] && echo "HEAD ok $H" || { echo "HEAD MISMATCH"; bad=1; }
[ "$(git rev-parse HEAD^{tree})" = "$T" ] && echo "tree ok $T" || { echo "TREE MISMATCH"; bad=1; }
[ "$(git write-tree)" = "$T" ] && echo "index tree ok" || { echo "INDEX MISMATCH"; bad=1; }
s=$(git status --porcelain=v1 --untracked-files=all); [ -z "$s" ] && echo "status clean (no modified/untracked)" || { echo "STATUS: $s"; bad=1; }
ig=$(git status --porcelain=v1 --ignored --untracked-files=all | grep '^!!' || true); [ -z "$ig" ] && echo "no ignored files" || echo "ignored: $ig"
flags=$(git ls-files -v | grep -v '^H ' || true); [ -z "$flags" ] && echo "no index flags" || { echo "INDEX FLAGS: $flags"; bad=1; }
n=0; m=0
while IFS= read -r line; do
  meta=${line%%	*}; path=${line#*	}; mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; sha=${rest#* }
  [ "$type" = blob ] || continue; n=$((n+1))
  if [ -L "$path" ]; then got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin); fm=120000
  else got=$(git hash-object --no-filters "$path"); [ -x "$path" ] && fm=100755 || fm=100644; fi
  [ "$got" = "$sha" ] && [ "$fm" = "$mode" ] || { echo "BLOB MISMATCH $path"; m=$((m+1)); }
done < <(git ls-tree -r HEAD)
echo "tracked blobs rehashed: $n, mismatches: $m"; [ $m -eq 0 ] || bad=1
git ls-tree -r HEAD | awk '$2=="commit"{print $3, $4}' | while read sha p; do
  w=$(git -C "$p" rev-parse HEAD 2>/dev/null || echo uninitialized); d=$(git -C "$p" status --porcelain 2>/dev/null | wc -l)
  echo "gitlink $p pinned $sha worktree $w dirty-lines $d"; done
exit $bad
