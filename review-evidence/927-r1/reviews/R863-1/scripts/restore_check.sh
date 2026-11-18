#!/bin/sh
# Verify a review clone is at the exact head with exact tracked bytes, modes,
# index and submodule gitlinks. usage: restore_check.sh <clone> <head-sha> <tree-sha>
set -u
C=$1; H=$2; T=$3
cd "$C" || exit 2
bad=0
say() { echo "$*"; }
[ "$(git rev-parse HEAD)" = "$H" ] && say "HEAD $H ok" || { say "HEAD mismatch: $(git rev-parse HEAD)"; bad=1; }
[ "$(git rev-parse HEAD^{tree})" = "$T" ] && say "tree $T ok" || { say "tree mismatch"; bad=1; }
# the index records exactly HEAD's tree (paths, modes, blob ids)
[ "$(git write-tree)" = "$T" ] && say "index writes tree $T: ok" || { say "index differs from HEAD's tree"; bad=1; }
# every tracked file's bytes and mode on disk equal the index (no stat cache trust)
git update-index -q --really-refresh >/dev/null 2>&1
if git diff --quiet --no-ext-diff && git diff --cached --quiet; then say "worktree and index equal HEAD: ok"; else say "worktree or index differs"; git diff --stat; bad=1; fi
# hidden-change flags would make the above blind
n=$(git ls-files -v | grep -c '^[a-zS]' || true)
[ "$n" = 0 ] && say "no assume-unchanged/skip-worktree entries: ok" || { say "$n hidden-change entries"; bad=1; }
# re-hash every tracked regular file from disk against the recorded blob id
mism=$(git ls-files -s | awk '$1 != "160000" {print $2" "$4}' | while read -r blob path; do
  [ "$(git hash-object --no-filters -- "$path")" = "$blob" ] || echo "$path"; done | wc -l)
[ "$mism" = 0 ] && say "every tracked file re-hashes to its blob: ok" || { say "$mism tracked files re-hash differently"; bad=1; }
# submodule gitlinks: recorded commit and the checkout's HEAD where initialised
git ls-files -s | awk '$1 == "160000" {print $2" "$4}' | while read -r sha path; do
  if [ -e "$path/.git" ]; then
    got=$(git -C "$path" rev-parse HEAD)
    [ "$got" = "$sha" ] && echo "gitlink $path $sha checkout ok" || echo "gitlink $path recorded $sha checkout $got MISMATCH"
  else
    echo "gitlink $path $sha (not initialised in this clone)"
  fi
done
u=$(git status --porcelain --untracked-files=all | wc -l)
i=$(git status --porcelain --ignored --untracked-files=all | grep -c '^!!' || true)
say "untracked entries: $u; ignored entries: $i"
[ "$u" = 0 ] || bad=1
echo "restore_check rc=$bad"
exit $bad
