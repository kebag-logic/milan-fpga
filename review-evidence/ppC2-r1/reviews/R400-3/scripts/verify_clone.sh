#!/usr/bin/env bash
# Verify the reviewer clone is exactly the reviewed head: HEAD, tree, index,
# every tracked blob's bytes and mode, no untracked or ignored entries, and
# the gitlink (submodule) set. Usage: verify_clone.sh <clone>
set -uo pipefail
C=$1
HEAD_EXP=921fff59d6e1243284e477f7a368173018420d35
TREE_EXP=dc1d52a75724f6ab29f4831d7498dece23202ca8
cd "$C" || exit 2
fail=0
h=$(git rev-parse HEAD); t=$(git rev-parse 'HEAD^{tree}'); w=$(git write-tree)
echo "HEAD $h"; echo "tree $t"; echo "write-tree $w"
[ "$h" = "$HEAD_EXP" ] || { echo "FAIL HEAD"; fail=1; }
[ "$t" = "$TREE_EXP" ] || { echo "FAIL tree"; fail=1; }
[ "$w" = "$TREE_EXP" ] || { echo "FAIL index tree"; fail=1; }
git update-index -q --really-refresh >/dev/null 2>&1
if git diff --quiet HEAD -- && git diff --cached --quiet HEAD --; then echo "worktree and index equal HEAD"; else echo "FAIL worktree/index differ"; fail=1; fi
u=$(git status --porcelain --ignored --untracked-files=all | wc -l)
echo "untracked or ignored entries: $u"; [ "$u" -eq 0 ] || { git status --porcelain --ignored --untracked-files=all | head; fail=1; }
n=0; bad=0
while IFS= read -r -d '' rec; do
  meta=${rec%%$'\t'*}; path=${rec#*$'\t'}
  mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; oid=${rest#* }
  n=$((n+1))
  if [ "$type" = blob ]; then
    got=$(git hash-object --no-filters -- "$path")
    if [ -L "$path" ]; then fm=120000; elif [ -x "$path" ]; then fm=100755; else fm=100644; fi
    if [ "$got" != "$oid" ] || [ "$fm" != "$mode" ]; then echo "FAIL $path"; bad=$((bad+1)); fi
  fi
done < <(git ls-tree -r -z HEAD)
echo "tracked entries checked: $n, mismatches: $bad"; [ "$bad" -eq 0 ] || fail=1
g=$(git ls-tree -r HEAD | awk '$2=="commit"' | wc -l)
echo "gitlinks at HEAD: $g"; [ -f .gitmodules ] && cat .gitmodules || echo "no .gitmodules: no submodule gitlinks are required"
echo "verdict: $([ $fail -eq 0 ] && echo CLEAN || echo DIRTY)"
exit $fail
