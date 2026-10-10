#!/usr/bin/env bash
# Verify a review clone is byte-exact at the expected head.
# Usage: clone_integrity.sh <repo> <head-sha> <tree-sha>
set -u
cd "$1" || exit 2
rc=0
say() { echo "$*"; }
[ "$(git rev-parse HEAD)" = "$2" ] && say "HEAD ok $2" || { say "HEAD MISMATCH $(git rev-parse HEAD)"; rc=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$3" ] && say "tree ok $3" || { say "TREE MISMATCH"; rc=1; }
[ "$(git write-tree)" = "$3" ] && say "index tree = HEAD tree" || { say "INDEX TREE MISMATCH"; rc=1; }
git diff --quiet && say "worktree = index" || { say "WORKTREE DIFFERS"; rc=1; }
git diff --cached --quiet && say "index = HEAD" || { say "INDEX DIFFERS"; rc=1; }
flags=$(git ls-files -v | grep -v '^H ' | head -5)
[ -z "$flags" ] && say "no assume-unchanged/skip-worktree flags" || { say "INDEX FLAGS: $flags"; rc=1; }
extra=$(git status --porcelain --ignored --untracked-files=all)
[ -z "$extra" ] && say "no untracked or ignored files" || { say "UNTRACKED/IGNORED:"; echo "$extra"; rc=1; }
# Rehash every tracked regular file and symlink; compare blob id and mode with HEAD.
bad=0; n=0
while read -r mode blob _stage path; do
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then
    got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
    [ -L "$path" ] || { echo "not a symlink: $path"; bad=$((bad+1)); continue; }
  else
    got=$(git hash-object --no-filters -- "$path")
    if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "mode: $path"; bad=$((bad+1)); }
    else [ -x "$path" ] && { echo "mode: $path"; bad=$((bad+1)); }; fi
  fi
  [ "$got" = "$blob" ] || { echo "blob: $path"; bad=$((bad+1)); }
done < <(git ls-files -s)
say "rehashed $n tracked files, $bad mismatches"; [ "$bad" = 0 ] || rc=1
say "gitlinks:"; git ls-files -s | awk '$1==160000'
git submodule status
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  [ -z "$(git -C "$s" status --porcelain 2>&1)" ] && say "submodule clean: $s" || { say "submodule dirty: $s"; rc=1; }
done
say "integrity rc=$rc"
exit $rc
