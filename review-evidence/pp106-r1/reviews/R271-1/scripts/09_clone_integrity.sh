#!/usr/bin/env bash
# Prove the review clone still holds the exact head: HEAD, tree, index,
# status, index flags, replace refs, gitlinks, and every tracked file's bytes
# (git hash-object --no-filters vs the HEAD blob id) and executable bit.
# Usage: 09_clone_integrity.sh <clone>
set -uo pipefail
cd "$1" || exit 2
export GIT_NO_REPLACE_OBJECTS=1
echo "HEAD $(git rev-parse HEAD)"
echo "HEAD^{tree} $(git rev-parse 'HEAD^{tree}')"
echo "write-tree(index) $(git write-tree)"
echo "status --porcelain --ignored lines: $(git status --porcelain --ignored | wc -l)"
echo "index vs HEAD changed paths: $(git diff --cached --name-only HEAD | wc -l)"
echo "worktree vs index changed paths: $(git diff --name-only | wc -l)"
echo "assume-unchanged/skip-worktree entries: $(git ls-files -v | grep -c -E '^[a-zS] ')"
echo "replace refs: $(git for-each-ref refs/replace | wc -l)"
echo "gitlinks (mode 160000) at HEAD: $(git ls-tree -r HEAD | awk '$1==160000' | wc -l)"
echo ".gitmodules present: $(test -e .gitmodules && echo yes || echo no)"
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  read -r mode _type sha <<<"$meta"
  [ "$mode" = 160000 ] && continue
  n=$((n + 1))
  h=$(git hash-object --no-filters -- "$path")
  if [ -x "$path" ]; then x=100755; else x=100644; fi
  if [ -L "$path" ]; then x=120000; fi
  if [ "$h" != "$sha" ] || [ "$x" != "$mode" ]; then
    echo "MISMATCH $path (blob $h vs $sha, mode $x vs $mode)"; bad=$((bad + 1))
  fi
done < <(git ls-tree -r HEAD)
echo "tracked files checked: $n, byte/mode mismatches: $bad"
