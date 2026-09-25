#!/usr/bin/env bash
# R300-4: prove the review clone is at the exact head with untouched bytes.
# Usage: verify_restore.sh <clone>
set -u
C=${1:?clone}
cd "$C" || exit 2
H=ddf8151c478fc54c98608589c1afe9525739d6a4
T=ea8460263670d159ab4c79005bd57de7d2326041
rc=0
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
[ "$(git rev-parse HEAD)" = "$H" ] || { echo "FAIL head"; rc=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$T" ] || { echo "FAIL tree"; rc=1; }
# Index tree equals the commit tree (modes, blob ids, gitlinks).
IT=$(git write-tree)
echo "index tree $IT"
[ "$IT" = "$T" ] || { echo "FAIL index"; rc=1; }
# Refresh stat data and require no worktree or index difference.
git update-index -q --really-refresh
git diff --quiet HEAD -- || { echo "FAIL worktree/index diff"; rc=1; }
git diff --cached --quiet || { echo "FAIL cached diff"; rc=1; }
# Rehash every tracked regular file against its recorded blob and mode.
bad=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; oid=${rest#* }
  [ "$type" = blob ] || continue
  if [ "$mode" = 120000 ]; then
    got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else
    got=$(git hash-object --no-filters -- "$path")
    fm=$([ -x "$path" ] && echo 100755 || echo 100644)
    [ "$fm" = "$mode" ] || { echo "MODE $path $fm != $mode"; bad=$((bad + 1)); }
  fi
  [ "$got" = "$oid" ] || { echo "BYTES $path"; bad=$((bad + 1)); }
done < <(git ls-tree -r --full-tree HEAD)
echo "tracked blob byte/mode mismatches: $bad"
[ "$bad" = 0 ] || rc=1
# Required submodule gitlinks: checked-out commit equals the recorded gitlink.
while read -r mode type oid path; do
  [ "$type" = commit ] || continue
  if [ -e "$path/.git" ]; then
    co=$(git -C "$path" rev-parse HEAD)
    st=$(git -C "$path" status --porcelain --ignored | wc -l)
    echo "gitlink $path $oid checked-out $co dirty-entries $st"
    [ "$co" = "$oid" ] && [ "$st" = 0 ] || rc=1
  else
    echo "gitlink $path $oid (not initialised)"
  fi
done < <(git ls-tree -r HEAD | awk '$2=="commit"{print $1, $2, $3, $4}')
echo "untracked+ignored entries: $(git status --porcelain --ignored | wc -l)"
[ "$(git status --porcelain --ignored | wc -l)" = 0 ] || rc=1
echo "rc=$rc"
exit $rc
