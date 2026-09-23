#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Reviewer integrity check: the clone is the exact head, every tracked blob's
# on-disk bytes and mode equal HEAD's, the index equals HEAD's tree, nothing
# is untracked or ignored, and the three gate submodules sit clean at their
# gitlinks. Usage: verify_clone.sh <clone> <expected head> <expected tree>
set -euo pipefail
clone=$1 head=$2 tree=$3
cd "$clone"
export GIT_NO_REPLACE_OBJECTS=1
fail=0
[ "$(git rev-parse HEAD)" = "$head" ] || { echo "FAIL: HEAD is $(git rev-parse HEAD)"; fail=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$tree" ] || { echo "FAIL: tree mismatch"; fail=1; }
[ "$(git write-tree)" = "$tree" ] || { echo "FAIL: index tree != head tree"; fail=1; }
# assume-unchanged / skip-worktree flags would hide edits from status
flagged=$(git ls-files -v | awk '$1 ~ /^([a-z]|S)$/' | wc -l)
[ "$flagged" -eq 0 ] || { echo "FAIL: $flagged index entries carry hide flags"; fail=1; }
# every regular tracked blob: bytes hash to HEAD's blob id, mode matches
checked=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; oid=${rest#* }
  case "$type" in
    blob)
      if [ "$mode" = 120000 ]; then
        [ -L "$path" ] && [ "$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)" = "$oid" ] \
          || { echo "FAIL: symlink $path"; fail=1; }
      else
        got=$(git hash-object --no-filters -- "$path")
        [ "$got" = "$oid" ] || { echo "FAIL: bytes $path"; fail=1; }
        if [ -x "$path" ]; then want=100755; else want=100644; fi
        [ "$want" = "$mode" ] || { echo "FAIL: mode $path ($want vs $mode)"; fail=1; }
      fi
      checked=$((checked + 1)) ;;
    commit)
      if [ -e "$path/.git" ]; then
        sub=$(git -C "$path" rev-parse HEAD 2>/dev/null || echo absent)
      else
        sub=uninitialised
      fi
      echo "gitlink $path $oid checkout $sub"
      case "$path" in
        gptp-processor|protocol-processor|third_party/verilog-axis)
          [ "$sub" = "$oid" ] || { echo "FAIL: $path checkout $sub != gitlink $oid"; fail=1; }
          [ -z "$(git -C "$path" status --porcelain=v1 --ignored)" ] \
            || { echo "FAIL: $path not clean"; fail=1; } ;;
      esac ;;
  esac
done < <(git ls-tree -r --full-tree HEAD)
extra=$(git status --porcelain=v1 --ignored --untracked-files=all | wc -l)
[ "$extra" -eq 0 ] || { echo "FAIL: $extra status lines"; git status --porcelain=v1 --ignored | head; fail=1; }
echo "tracked blobs checked: $checked"
[ "$fail" -eq 0 ] && echo "RESULT: PASS (exact head bytes, modes, index and gitlinks)" || echo "RESULT: FAIL"
exit "$fail"
