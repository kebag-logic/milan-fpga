#!/usr/bin/env bash
# Verify the review clone still holds exact-head bytes, index, modes and gitlinks.
# Usage: verify_clone_state.sh <repo> <expected head> <expected tree>
set -u
cd "$1" || exit 2
fail=0
[ "$(git rev-parse HEAD)" = "$2" ] && echo "HEAD ok $2" || { echo "HEAD MISMATCH"; fail=1; }
[ "$(git rev-parse HEAD^{tree})" = "$3" ] && echo "tree ok $3" || { echo "TREE MISMATCH"; fail=1; }
# index entries (mode, object, stage 0, path) must equal the HEAD tree exactly
if diff <(git ls-files -s | awk '{print $1" "$2" "$3" "$4}') \
        <(git ls-tree -r --full-tree HEAD | awk '{print $1" "$3" 0 "$4}') >/dev/null; then
  echo "index == HEAD tree (modes, objects, stage 0)"; else echo "INDEX MISMATCH"; fail=1; fi
# no hidden-index flags
n=$(git ls-files -v | grep -vc '^H ')
[ "$n" = 0 ] && echo "no assume-unchanged/skip-worktree entries" || { echo "HIDDEN FLAGS: $n"; fail=1; }
# re-hash every regular tracked file from disk (no stat shortcut)
bad=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1 obj=$3
  [ "$mode" = 160000 ] && continue
  if [ "$mode" = 120000 ]; then
    [ "$(printf %s "$(readlink "$path")" | git hash-object --stdin)" = "$obj" ] || { echo "SYMLINK DIFF $path"; bad=1; }
  else
    [ "$(git hash-object --no-filters -- "$path")" = "$obj" ] || { echo "BLOB DIFF $path"; bad=1; }
    x=$([ -x "$path" ] && echo 100755 || echo 100644)
    [ "$x" = "$mode" ] || { echo "MODE DIFF $path"; bad=1; }
  fi
done < <(git ls-tree -r --full-tree HEAD)
[ $bad = 0 ] && echo "every tracked blob re-hashed from disk equals HEAD, modes equal" || fail=1
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  want=$(git rev-parse "HEAD:$s"); have=$(git -C "$s" rev-parse HEAD 2>/dev/null)
  dirty=$(git -C "$s" status --porcelain 2>/dev/null | wc -l)
  [ "$want" = "$have" ] && [ "$dirty" = 0 ] && echo "gitlink ok $s $want clean" || { echo "GITLINK MISMATCH $s want=$want have=$have dirty=$dirty"; fail=1; }
done
echo "untracked (not ignored): $(git status --porcelain --untracked-files=all | grep -c '^??')"
git status --porcelain | head
echo "RESULT $([ $fail = 0 ] && echo PASS || echo FAIL)"
exit $fail
