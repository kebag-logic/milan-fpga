#!/usr/bin/env bash
# Prove a checkout still holds the exact committed bytes of HEAD.
# Usage: verify_integrity.sh <checkout> <expected-head> <expected-tree>
# Checks: HEAD/tree identity; index equals HEAD's tree (write-tree); every
# tracked regular file's on-disk bytes hash to its index blob and its mode
# matches; no tracked-path worktree change; required submodule gitlinks are
# stage-0 160000 records whose checkout HEAD equals the gitlink; no untracked
# files outside ignored paths. Prints one line per check; exit 0 only if all pass.
set -uo pipefail
repo=${1:?checkout}
want_head=${2:?head}
want_tree=${3:?tree}
cd "$repo" || exit 2
export GIT_NO_REPLACE_OBJECTS=1
fail=0
chk() { if [ "$2" = "$3" ]; then echo "PASS $1"; else echo "FAIL $1 want=$3 got=$2"; fail=1; fi; }

chk head "$(git rev-parse HEAD)" "$want_head"
chk tree "$(git rev-parse 'HEAD^{tree}')" "$want_tree"
chk index-tree "$(git write-tree)" "$want_tree"

bad=0; count=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; blob=${rest%% *}; stage=${rest##* }
  [ "$stage" = 0 ] || { echo "FAIL stage $path $stage"; bad=1; continue; }
  case "$mode" in
    160000) continue ;;
    120000)
      got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin) ;;
    100644|100755)
      if [ -L "$path" ] || [ ! -f "$path" ]; then echo "FAIL type $path"; bad=1; continue; fi
      got=$(git hash-object --no-filters -- "$path")
      if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "FAIL mode $path"; bad=1; fi
      if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "FAIL mode $path"; bad=1; fi ;;
    *) echo "FAIL unknown-mode $mode $path"; bad=1; continue ;;
  esac
  count=$((count + 1))
  [ "$got" = "$blob" ] || { echo "FAIL bytes $path"; bad=1; }
done < <(git ls-files -s)
chk "tracked-bytes-and-modes ($count files)" "$bad" 0

chk worktree-diff "$(git diff --name-only | wc -l)" 0
chk cached-diff "$(git diff --cached --name-only | wc -l)" 0
chk untracked "$(git ls-files --others --exclude-standard | wc -l)" 0

for sub in third_party/verilog-axis protocol-processor gptp-processor; do
  rec=$(git ls-files -s -- "$sub")
  mode=${rec%% *}; rest=${rec#* }; pin=${rest%% *}
  chk "gitlink-mode $sub" "$mode" 160000
  chk "gitlink-records $sub" "$(printf '%s\n' "$rec" | grep -c .)" 1
  chk "gitlink-in-HEAD $sub" "$(git rev-parse "HEAD:$sub")" "$pin"
  chk "checkout-head $sub" "$(git -C "$sub" rev-parse HEAD 2>/dev/null)" "$pin"
  chk "checkout-clean $sub" "$(git -C "$sub" status --porcelain --untracked-files=no | wc -l)" 0
done
echo "OVERALL $([ $fail = 0 ] && echo PASS || echo FAIL)"
exit $fail
