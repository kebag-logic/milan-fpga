#!/usr/bin/env bash
# Verify a review clone is byte-exact at the expected head.
# usage: clone_integrity.sh <clone-dir> <expected-head> <expected-tree>
set -u
cd "$1" || exit 2
head=$2 tree=$3 rc=0
export GIT_NO_REPLACE_OBJECTS=1
g() { command git -c core.pager=cat "$@"; }
[ "$(g rev-parse HEAD)" = "$head" ] && echo "HEAD ok $head" || { echo "HEAD MISMATCH"; rc=1; }
[ "$(g rev-parse 'HEAD^{tree}')" = "$tree" ] && echo "HEAD tree ok $tree" || { echo "TREE MISMATCH"; rc=1; }
[ "$(g write-tree)" = "$tree" ] && echo "index tree ok" || { echo "INDEX TREE MISMATCH"; rc=1; }
st=$(g status --porcelain=v1 --untracked-files=all)
[ -z "$st" ] && echo "status clean (0 untracked)" || { echo "STATUS DIRTY:"; echo "$st"; rc=1; }
flags=$(g ls-files -v | grep -v '^H ' | grep -v '^S ' ; g ls-files -v | grep -E '^(h|S) ' )
[ -z "$flags" ] && echo "no assume-unchanged/skip-worktree flags" || { echo "INDEX FLAGS:"; echo "$flags" | head; rc=1; }
n=0 bad=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1 sha=$3
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then
    got=$(printf '%s' "$(readlink -- "$path")" | g hash-object --stdin)
  else
    got=$(g hash-object --no-filters -- "$path")
    fm=$(stat -c %a -- "$path"); case "$mode:$fm" in 100755:7??|100644:6??) ;; *) echo "MODE DRIFT $mode $fm $path"; bad=$((bad+1));; esac
  fi
  [ "$got" = "$sha" ] || { echo "BLOB MISMATCH $path"; bad=$((bad+1)); }
done < <(g ls-tree -r HEAD)
echo "tracked non-gitlink entries rehashed: $n, mismatches/mode drift: $bad"
[ $bad -eq 0 ] || rc=1
echo "gitlinks at HEAD vs submodule checkouts:"
while IFS=$'\t' read -r meta path; do
  set -- $meta; [ "$1" = 160000 ] || continue
  if [ -e "$path/.git" ]; then cur=$(g -C "$path" rev-parse HEAD 2>/dev/null); else cur="(not initialised)"; fi
  [ "$cur" = "$3" ] && echo "  $path pin ${3:0:12} checkout ok" || echo "  $path pin ${3:0:12} checkout $cur"
done < <(g ls-tree -r HEAD)
g submodule status 2>&1 | sed 's/^/  submodule status: /'
echo "RESULT $([ $rc -eq 0 ] && echo PASS || echo FAIL)"
exit $rc
