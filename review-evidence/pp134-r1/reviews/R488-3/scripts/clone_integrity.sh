#!/bin/bash
# clone_integrity.sh CLONE HEAD TREE : prove the review clone holds exact head bytes.
set -u
c=$1; head=$2; tree=$3
cd "$c" || exit 2
echo "HEAD $(git rev-parse HEAD) (want $head)"; echo "TREE $(git rev-parse HEAD^{tree}) (want $tree)"
echo "status-porcelain-ignored-lines $(git status --porcelain --ignored | wc -l)"
echo "diff-worktree-lines $(git diff | wc -l) diff-index-lines $(git diff --cached | wc -l)"
idx=$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum | cut -c1-64)
lst=$(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sha256sum | cut -c1-64)
echo "index-vs-tree $([ "$idx" = "$lst" ] && echo EQUAL || echo DIFFER) ($idx)"
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1; blob=$3; n=$((n+1))
  [ "$mode" = 160000 ] && { echo "gitlink $path $blob"; continue; }
  if [ "$mode" = 120000 ]; then got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin)
  else got=$(git hash-object --no-filters -- "$path"); fi
  [ "$got" = "$blob" ] || { echo "BLOB MISMATCH $path"; bad=$((bad+1)); }
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "MODE MISMATCH $path"; bad=$((bad+1)); }
  elif [ "$mode" = 100644 ]; then [ -x "$path" ] && { echo "MODE MISMATCH $path"; bad=$((bad+1)); }; fi
done < <(git ls-tree -r HEAD)
echo "files $n blob-or-mode-mismatches $bad gitlinks $(git ls-tree -r HEAD | awk '$1==160000' | wc -l)"
