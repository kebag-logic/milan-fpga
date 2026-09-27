#!/bin/bash
# Verify the review clone still holds the exact reviewed head: index == HEAD tree,
# every tracked worktree blob and mode matches the index, no hidden index flags,
# and the three required submodule gitlinks are checked out at their pins.
# Usage: verify_clone_integrity.sh <clone> <expected-head> <expected-tree>
set -u
cd "$1" || exit 2
fail=0
[ "$(git rev-parse HEAD)" = "$2" ] && echo "HEAD ok $2" || { echo "HEAD MISMATCH"; fail=1; }
[ "$(git rev-parse HEAD^{tree})" = "$3" ] && echo "tree ok $3" || { echo "TREE MISMATCH"; fail=1; }
[ "$(git write-tree)" = "$3" ] && echo "index tree == HEAD tree" || { echo "INDEX DIFFERS"; fail=1; }
flags=$(git ls-files -v | grep -v '^H ' | grep -v '^S ' || true)
hidden=$(git ls-files -v | grep -c '^[a-zS] ' || true)
[ "$hidden" = 0 ] && echo "no assume-unchanged/skip-worktree entries" || { echo "HIDDEN FLAGS: $hidden"; fail=1; }
mism=0; n=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; blob=${rest%% *}
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else got=$(git hash-object --no-filters -- "$path" 2>/dev/null)
    if [ -x "$path" ]; then fm=100755; else fm=100644; fi
    [ "$fm" = "$mode" ] || { echo "MODE $path index=$mode fs=$fm"; mism=$((mism+1)); }
  fi
  [ "$got" = "$blob" ] || { echo "BYTES $path"; mism=$((mism+1)); }
done < <(git ls-files -s)
echo "tracked non-gitlink entries checked: $n, mismatches: $mism"; [ "$mism" = 0 ] || fail=1
for sm in protocol-processor gptp-processor third_party/verilog-axis; do
  pin=$(git rev-parse ":$sm"); head=$(git -C "$sm" rev-parse HEAD)
  dirty=$(git -C "$sm" status --porcelain | wc -l)
  [ "$pin" = "$head" ] && [ "$dirty" = 0 ] && echo "submodule $sm at pin $pin, clean" || { echo "SUBMODULE $sm pin=$pin head=$head dirty=$dirty"; fail=1; }
done
echo "untracked (non-ignored): $(git status --porcelain --untracked-files=all | grep -c '^??' || true)"
echo "RESULT: $([ $fail = 0 ] && echo INTACT || echo NOT-INTACT)"; exit $fail
