#!/usr/bin/env bash
# Usage: verify_restore.sh <repository> <expected head> <expected tree>
# Verifies HEAD/tree, an empty status including ignored files, index entries
# equal to the HEAD tree, every regular tracked file re-hashing to its blob with
# the recorded mode, the gitlinks, and clean initialised submodule worktrees.
set -u
repo=$1; head=$2; tree=$3
cd "$repo" || exit 2
fail=0
note() { echo "$*"; }
bad() { echo "FAIL: $*"; fail=1; }
[ "$(git rev-parse HEAD)" = "$head" ] && note "HEAD $head" || bad "HEAD $(git rev-parse HEAD)"
[ "$(git rev-parse HEAD^{tree})" = "$tree" ] && note "tree $tree" || bad "tree"
st=$(git status --porcelain=v1 --ignored --ignore-submodules=none 2>/dev/null)
[ -z "$st" ] && note "status (including ignored): empty" || bad "status: $st"
idx=$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum)
hd=$(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sha256sum)
[ "$idx" = "$hd" ] && note "index entries equal HEAD tree ($(git ls-files -s | wc -l) entries)" || bad "index differs from HEAD tree"
n=0
while read -r mode blob _stage path; do
  [ "$mode" = 160000 ] && continue
  n=$((n + 1))
  if [ "$mode" = 120000 ]; then
    got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else
    got=$(git hash-object --no-filters -- "$path")
    if [ "$mode" = 100755 ]; then [ -x "$path" ] || bad "mode $path"; else [ ! -x "$path" ] || bad "mode $path"; fi
  fi
  [ "$got" = "$blob" ] || bad "bytes $path"
done < <(git ls-files -s)
note "re-hashed $n non-gitlink tracked files"
while read -r mode _type sha path; do
  if [ -e "$path/.git" ]; then
    got=$(git -C "$path" rev-parse HEAD)
    [ "$got" = "$sha" ] || bad "gitlink $path at $got, want $sha"
    s=$(git -C "$path" status --porcelain --ignored)
    [ -z "$s" ] || bad "submodule $path dirty: $s"
    note "gitlink $path $sha (initialised, clean)"
  else
    note "gitlink $path $sha (not initialised)"
  fi
done < <(git ls-tree -r HEAD | awk '$1 == "160000"')
[ "$fail" = 0 ] && echo "RESTORE VERIFIED" || echo "RESTORE VERIFICATION FAILED"
exit "$fail"
