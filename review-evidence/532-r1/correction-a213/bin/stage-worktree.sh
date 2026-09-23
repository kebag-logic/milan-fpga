#!/usr/bin/env bash
# [A213] Refresh a disposable stage clone with the lane worktree's current
# files (committed head plus uncommitted edits to the lane's four files), so
# the candidate self-test never runs from the lane worktree itself.
# Usage: stage-worktree.sh LANE STAGE
set -euo pipefail
lane=$1 stage=$2
if [ ! -d "$stage/.git" ]; then git clone --quiet --no-hardlinks "$lane" "$stage"; fi
git -C "$stage" fetch --quiet "$lane" HEAD
git -C "$stage" checkout --quiet --force FETCH_HEAD
git -C "$stage" clean --quiet -fdx
for f in scripts/act_ci.py scripts/act_slot_proof.sh scripts/check_baremetal_only.py docs/testing/CI_WORKFLOWS.md; do
  cp -p "$lane/$f" "$stage/$f"
done
echo "stage $(git -C "$stage" rev-parse --short HEAD) + worktree: $(git -C "$stage" status --porcelain | tr '\n' ' ')"
