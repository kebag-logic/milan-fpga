#!/usr/bin/env bash
# Export a commit of the lane plus its three pinned submodules into a scratch tree
# (git archive; nothing in the lane is written). protocol-processor gets a scratch-local
# git repo so scripts/pp_srcs.py (git ls-files) can list the processor sources.
#   export.sh <rev> <dest>
set -euo pipefail
LANE=$LANES/617-capture-frame-atomic
rev=$1; dest=$2
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.commitGraph GIT_CONFIG_VALUE_0=false
[ -e "$dest" ] && { echo "exists: $dest" >&2; exit 1; }
mkdir -p "$dest"
git -C "$LANE" archive "$rev" | tar -x -C "$dest"
for s in protocol-processor third_party/verilog-axis gptp-processor; do
  top=$(git -C "$LANE/$s" rev-parse --show-toplevel)
  [ "$top" = "$LANE/$s" ] || { echo "submodule toplevel mismatch: $s -> $top" >&2; exit 1; }
  pin=$(git -C "$LANE" ls-tree "$rev" "$s" | awk '{print $3}')
  mkdir -p "$dest/$s"
  git -C "$LANE/$s" archive "$pin" | tar -x -C "$dest/$s"
  echo "$s $pin"
done
( cd "$dest/protocol-processor" && git init -q && git add -A && \
  git -c user.name=scratch -c user.email=scratch@invalid commit -qm scratch )
echo "exported $rev -> $dest (tree $(git -C "$LANE" rev-parse "$rev^{tree}"))"
