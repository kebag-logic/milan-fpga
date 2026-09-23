#!/usr/bin/env bash
# Record the exact tracked state of a clone: HEAD, tree, index records
# (mode/blob/stage/path), a byte hash of every tracked worktree file, the
# submodule gitlinks and checkouts, and porcelain status. Two snapshots that
# compare equal prove the probes left the tracked bytes, modes and index as found.
# usage: snapshot_state.sh <clone> <out-file>
set -euo pipefail
clone=$1; out=$2
cd "$clone"
{
  echo "HEAD $(git rev-parse HEAD)"
  echo "TREE $(git rev-parse 'HEAD^{tree}')"
  echo "INDEX-TREE $(git write-tree)"
  echo "## index records sha256: $(git ls-files -s | sha256sum | cut -d' ' -f1)"
  echo "## worktree bytes of tracked regular files (hash-object) vs index"
  git ls-files -s | awk '$1!="160000"{print $4}' | git hash-object --stdin-paths --no-filters > /tmp/.snap_wt.$$ 
  git ls-files -s | awk '$1!="160000"{print $2}' > /tmp/.snap_ix.$$
  if cmp -s /tmp/.snap_wt.$$ /tmp/.snap_ix.$$; then echo "WORKTREE-BYTES == INDEX-BLOBS"; else echo "WORKTREE-BYTES DIFFER"; paste /tmp/.snap_ix.$$ /tmp/.snap_wt.$$ | awk '$1!=$2' | head; fi
  echo "## worktree modes"
  git ls-files -s | awk '$1!="160000"{print $1, $4}' | while read -r m p; do
    x=100644; [ -x "$p" ] && x=100755; [ -L "$p" ] && x=120000; [ "$x" = "$m" ] || echo "MODE-DIFF $p index=$m worktree=$x"; done
  echo "## gitlinks"
  git ls-files -s | awk '$1=="160000"'
  for s in third_party/verilog-axis protocol-processor gptp-processor; do
    echo "checkout $s $(git -C "$s" rev-parse HEAD) dirty=$(git -C "$s" status --porcelain | wc -l)"
  done
  echo "## status (untracked and modified, ignored excluded)"
  git status --porcelain=v1
  echo "## end"
} > "$out"
rm -f /tmp/.snap_wt.$$ /tmp/.snap_ix.$$
