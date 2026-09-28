#!/usr/bin/env bash
# Make a disposable shared clone of <clone> at <rev> with the three initialised
# submodules (worktree bytes and git metadata copied, so `git ls-files` works
# inside them). The reviewed clone is only read.
# Usage: mkclone.sh <clone> <rev> <dest>
set -euo pipefail
clone=$1 rev=$2 d=$3
rm -rf "$d"
git clone -q --shared --no-checkout "$clone" "$d"
git -C "$d" checkout -q --detach "$rev"
for sub in protocol-processor gptp-processor third_party/verilog-axis; do
  rm -rf "${d:?}/$sub"; mkdir -p "$(dirname "$d/$sub")" "$(dirname "$d/.git/modules/$sub")"
  cp -a "$clone/$sub" "$d/$sub"
  cp -a "$clone/.git/modules/$sub" "$d/.git/modules/$sub"
done
echo "clone $d at $(git -C "$d" rev-parse HEAD) tree $(git -C "$d" rev-parse HEAD^{tree})"
for sub in protocol-processor gptp-processor third_party/verilog-axis; do echo "  $sub HEAD=$(git -C "$d/$sub" rev-parse HEAD) gitlink=$(git -C "$d" rev-parse "HEAD:$sub")"; done
echo "dirty=$(git -C "$d" status --porcelain --ignore-submodules=none | wc -l)"
