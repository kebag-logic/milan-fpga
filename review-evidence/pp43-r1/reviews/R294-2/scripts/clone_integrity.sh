#!/usr/bin/env bash
# R294 clone integrity: the review clone must still be byte- and mode-identical
# to the exact head. Read-only (git write-tree only writes a tree object that
# already exists when the index is unchanged).
# Usage: clone_integrity.sh <clone> <expected-head> <expected-tree>
set -uo pipefail
clone=$1; head=$2; tree=$3
cd "$clone" || exit 2
rc=0
h=$(git rev-parse HEAD); t=$(git rev-parse HEAD^{tree}); w=$(git write-tree)
echo "HEAD        $h"; echo "HEAD^{tree} $t"; echo "write-tree  $w"
[ "$h" = "$head" ] && [ "$t" = "$tree" ] && [ "$w" = "$tree" ] || { echo "MISMATCH head/tree/index"; rc=1; }
st=$(git status --porcelain=v1 --ignored --untracked-files=all)
if [ -n "$st" ]; then echo "worktree NOT clean:"; echo "$st" | head -20; rc=1; else echo "worktree clean (no modified, untracked or ignored files)"; fi
git diff --quiet HEAD -- || { echo "diff vs HEAD non-empty"; rc=1; }
git diff --cached --quiet HEAD -- || { echo "index differs from HEAD"; rc=1; }
# per-file blob and mode re-hash from the worktree against HEAD's tree
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; oid=${rest#* }
  n=$((n+1))
  if [ "$type" = "commit" ]; then echo "gitlink $path $oid"; continue; fi
  got=$(git hash-object -- "$path")
  if [ -L "$path" ]; then fm=120000; elif [ -x "$path" ]; then fm=100755; else fm=100644; fi
  if [ "$got" != "$oid" ] || [ "$fm" != "$mode" ]; then echo "DIFF $path want $mode $oid got $fm $got"; bad=$((bad+1)); fi
done < <(git ls-tree -r --full-tree HEAD)
echo "tracked entries re-hashed: $n, mismatches: $bad"
[ "$bad" -eq 0 ] || rc=1
echo "gitlinks (mode 160000): $(git ls-tree -r HEAD | awk '$1=="160000"' | wc -l)"
echo "integrity rc=$rc"
exit "$rc"
