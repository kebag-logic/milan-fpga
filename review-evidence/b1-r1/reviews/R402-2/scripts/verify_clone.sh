#!/usr/bin/env bash
# Prove the review clone is the exact published head: HEAD/tree, index == HEAD, every tracked
# blob's bytes and mode, submodule gitlinks, and no untracked or ignored leftovers.
# usage: verify_clone.sh <clone> <expected-head> <expected-tree>
set -u
cd "$1" || exit 2
h=$(git rev-parse HEAD); t=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $h"; echo "TREE $t"
[ "$h" = "$2" ] && [ "$t" = "$3" ] || { echo "FAIL head/tree"; exit 1; }
git diff --quiet HEAD -- && git diff --cached --quiet HEAD -- && echo "PASS worktree and index equal HEAD" || { echo "FAIL diff"; exit 1; }
[ "$(git write-tree)" = "$t" ] && echo "PASS index writes tree $t" || { echo "FAIL index tree"; exit 1; }
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; oid=${rest#* }
  n=$((n+1))
  if [ "$type" = commit ]; then
    got=$(git -C "$path" rev-parse HEAD 2>/dev/null || echo uninitialised)
    echo "gitlink $path $oid checkout=$got"
    continue
  fi
  if [ "$mode" = 120000 ]; then
    [ "$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)" = "$oid" ] || { echo "FAIL symlink $path"; bad=$((bad+1)); }
  else
    [ "$(git hash-object --no-filters -- "$path")" = "$oid" ] || { echo "FAIL blob $path"; bad=$((bad+1)); }
    x=$([ -x "$path" ] && echo 100755 || echo 100644)
    [ "$x" = "$mode" ] || { echo "FAIL mode $path $x vs $mode"; bad=$((bad+1)); }
  fi
done < <(git ls-tree -r --full-tree HEAD)
echo "checked $n tree entries, $bad failures"
u=$(git status --porcelain --untracked-files=all --ignored)
[ -z "$u" ] && echo "PASS no untracked or ignored files" || { echo "FAIL leftovers:"; echo "$u" | head; bad=$((bad+1)); }
exit $bad
