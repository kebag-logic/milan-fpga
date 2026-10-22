#!/usr/bin/env bash
# Usage: verify_clone.sh REPO - exact head, clean tracked bytes/modes, index == HEAD tree, gitlinks and submodule HEADs.
set -u; R=$1; rc=0
h=$(git -C "$R" rev-parse HEAD); t=$(git -C "$R" rev-parse 'HEAD^{tree}')
echo "head $h tree $t"; [ "$h" = a97aea01449492b1f640924f5a34726f602cabed ] && [ "$t" = ea69f3b4c4c4b2f50a38a868b5f1dba56b248249 ] || rc=1
git -C "$R" update-index -q --really-refresh >/dev/null 2>&1
git -C "$R" diff --quiet HEAD -- || { echo "worktree differs from HEAD"; rc=1; }
git -C "$R" diff --cached --quiet HEAD -- || { echo "index differs from HEAD"; rc=1; }
[ "$(git -C "$R" write-tree)" = "$t" ] && echo "index tree == HEAD tree" || { echo "index tree differs"; rc=1; }
u=$(git -C "$R" status --porcelain --untracked-files=normal | grep -v '^!!' | wc -l); echo "untracked/modified entries (non-ignored): $u"; [ "$u" = 0 ] || rc=1
for m in protocol-processor:93fb0b2d736b36588ea7321e25fba2f8819ea41f gptp-processor:55680bff3b287b9a7b0c759f51471fa617c17335; do
  p=${m%%:*}; s=${m#*:}; gl=$(git -C "$R" rev-parse "HEAD:$p"); sh=$(git -C "$R/$p" rev-parse HEAD); d=$(git -C "$R/$p" status --porcelain | wc -l)
  echo "$p gitlink=$gl checkout=$sh dirty_entries=$d"; [ "$gl" = "$s" ] && [ "$sh" = "$s" ] && [ "$d" = 0 ] || rc=1; done
echo "verify rc=$rc"; exit $rc
