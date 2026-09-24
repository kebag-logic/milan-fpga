#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Verify a review clone is exactly the reviewed head: HEAD/tree, clean index
# and worktree, no untracked/ignored files, every tracked blob's bytes and
# mode, and the gitlink (submodule) list.
# Usage: verify_clone.sh <clone> <head-sha> <tree-sha>
set -uo pipefail
C=$1; HEAD=$2; TREE=$3; rc=0
cd "$C" || exit 2
[ "$(git rev-parse HEAD)" = "$HEAD" ] && echo "HEAD $HEAD OK" || { echo "HEAD MISMATCH"; rc=1; }
[ "$(git rev-parse HEAD^{tree})" = "$TREE" ] && echo "tree $TREE OK" || { echo "tree MISMATCH"; rc=1; }
[ "$(git write-tree)" = "$TREE" ] && echo "index tree OK" || { echo "index tree MISMATCH"; rc=1; }
git diff --quiet && echo "worktree vs index clean" || { echo "worktree DIRTY"; rc=1; }
git diff --cached --quiet && echo "index vs HEAD clean" || { echo "index DIRTY"; rc=1; }
extra=$(git status --porcelain=v1 --untracked-files=all --ignored)
[ -z "$extra" ] && echo "no untracked/ignored files" || { echo "EXTRA FILES:"; echo "$extra"; rc=1; }
n=0; bad=0
while read -r mode sha _stage path; do
  n=$((n+1))
  case $mode in
    160000) continue ;;
    120000) got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin) ;;
    *)      got=$(git hash-object --no-filters -- "$path")
            if [ -x "$path" ]; then fm=100755; else fm=100644; fi
            [ "$fm" = "$mode" ] || { echo "MODE MISMATCH $path $fm != $mode"; bad=$((bad+1)); } ;;
  esac
  [ "$got" = "$sha" ] || { echo "BLOB MISMATCH $path"; bad=$((bad+1)); }
done < <(git ls-files -s)
echo "tracked entries: $n, byte/mode mismatches: $bad"
[ "$bad" -eq 0 ] || rc=1
gl=$(git ls-files -s | awk '$1=="160000"')
echo "gitlinks: ${gl:-none}"
exit $rc
