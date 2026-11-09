#!/bin/sh
# clean_tree.sh SRC DEST : clone SRC's committed HEAD into DEST with the submodules
# the milan_dp legs and the firmware tests read, each at its gitlink, from SRC's own clones.
set -eu
SRC=$1; DEST=$2
HEAD=$(git -C "$SRC" rev-parse HEAD)
git clone --quiet --no-checkout "$SRC" "$DEST"
git -C "$DEST" -c advice.detachedHead=false checkout --quiet --detach "$HEAD"
for p in third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP; do
  name=$(git -C "$DEST" config --file .gitmodules --get-regexp '^submodule\..*\.path$' | awk -v p="$p" '$2==p{print $1}' | sed 's/\.path$//')
  git -C "$DEST" submodule init -- "$p" >/dev/null
  git -C "$DEST" config "$name.url" "$SRC/$p"
  git -C "$DEST" -c protocol.file.allow=always submodule update --quiet -- "$p"
done
test -z "$(git -C "$DEST" status --porcelain)"
echo "clean tree $DEST at $(git -C "$DEST" rev-parse HEAD) tree $(git -C "$DEST" rev-parse HEAD^{tree})"
git -C "$DEST" submodule status | cat
