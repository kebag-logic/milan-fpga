#!/usr/bin/env bash
# Prove the review clone still holds the exact head bytes: HEAD, tree, index,
# worktree blobs and modes, no stray files, and the gitlink inventory.
# Receipt: receipts/clone-verify.txt
source "$(dirname "$0")/common.sh"
{
  echo "HEAD $(git -C "$CLONE" rev-parse HEAD) (want $HEAD_SHA)"
  echo "tree $(git -C "$CLONE" rev-parse 'HEAD^{tree}') (want $HEAD_TREE)"
  echo "index-tree $(git -C "$CLONE" write-tree) (want $HEAD_TREE)"
  git -C "$CLONE" update-index -q --really-refresh >/dev/null 2>&1 || true
  git -C "$CLONE" diff --quiet && echo "worktree vs index: identical (content+mode)" || echo "worktree vs index: DIFFERS"
  git -C "$CLONE" diff --cached --quiet HEAD && echo "index vs HEAD: identical" || echo "index vs HEAD: DIFFERS"
  echo "status --porcelain --ignored (empty = no untracked/ignored files):"
  git -C "$CLONE" status --porcelain --ignored
  echo "--- end status"
  # independent blob re-hash of every tracked regular file
  bad=0
  while read -r mode sha _stage path; do
    [ "$mode" = 160000 ] && continue
    [ "$(git -C "$CLONE" hash-object "$path")" = "$sha" ] || { echo "BLOB MISMATCH $path"; bad=$((bad+1)); }
    if [ "$mode" = 100755 ]; then [ -x "$CLONE/$path" ] || { echo "MODE MISMATCH $path"; bad=$((bad+1)); }; fi
  done < <(git -C "$CLONE" ls-files -s)
  echo "tracked files re-hashed: $(git -C "$CLONE" ls-files | wc -l), mismatches: $bad"
  echo "gitlinks (mode 160000) at head:"
  git -C "$CLONE" ls-tree -r HEAD | awk '$1=="160000"' ; echo "--- end gitlinks (none listed = this repository has no submodules)"
} >"$RECEIPTS/clone-verify.txt" 2>&1
cat "$RECEIPTS/clone-verify.txt"
