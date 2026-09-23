#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer receipt script: prove the review clone still holds the exact head.
# Usage: verify_clone.sh <clone> <head sha> <head tree>
set -uo pipefail
clone=${1:?clone}; head=${2:?head}; tree=${3:?tree}
cd "$clone" || exit 2
rc=0
h=$(git rev-parse HEAD); t=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $h"; echo "tree $t"
[ "$h" = "$head" ] || { echo "HEAD MISMATCH"; rc=1; }
[ "$t" = "$tree" ] || { echo "TREE MISMATCH"; rc=1; }
# the index must equal HEAD's tree
it=$(git write-tree 2>/dev/null) || it="(unwritable index)"
echo "index tree $it"; [ "$it" = "$tree" ] || { echo "INDEX MISMATCH"; rc=1; }
git diff --cached --quiet || { echo "STAGED CHANGES"; rc=1; }
git diff --quiet || { echo "WORKTREE CHANGES"; rc=1; }
# every tracked path: worktree bytes hash to the recorded blob, mode matches
n=0; bad=0
while read -r mode blob _stage path; do
  n=$((n + 1))
  if [ "$mode" = "160000" ]; then echo "gitlink $path $blob"; continue; fi
  wb=$(git hash-object --no-filters -- "$path" 2>/dev/null) || wb=missing
  if [ -L "$path" ]; then wm=120000; elif [ -x "$path" ]; then wm=100755; else wm=100644; fi
  if [ "$wb" != "$blob" ] || [ "$wm" != "$mode" ]; then
    echo "DIFF $path recorded=$mode:$blob worktree=$wm:$wb"; bad=$((bad + 1))
  fi
done < <(git ls-files -s)
echo "tracked entries checked: $n, differing: $bad"
[ "$bad" -eq 0 ] || rc=1
gl=$(git ls-files -s | awk '$1=="160000"' | wc -l)
echo "gitlinks (submodules) recorded at HEAD: $gl; .gitmodules present: $([ -f .gitmodules ] && echo yes || echo no)"
echo "untracked or ignored files:"; git status --porcelain --ignored --untracked-files=all | sed 's/^/  /'
[ -z "$(git status --porcelain --ignored --untracked-files=all)" ] || rc=1
echo "rc=$rc"; exit "$rc"
