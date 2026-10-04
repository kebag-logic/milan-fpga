#!/bin/sh
# mk_tree.sh SRC_CLONE DEST REV - shared, detached clone of SRC_CLONE at REV with the
# three build submodules checked out at REV's gitlinks (read-only use of SRC_CLONE).
set -e
C=$1; d=$2; rev=$3
git clone -q --shared --no-checkout "$C" "$d"
git -C "$d" checkout -q --detach "$rev"
for sm in protocol-processor gptp-processor third_party/verilog-axis; do
  oid=$(git -C "$C" ls-tree "$rev" "$sm" | awk '{print $3}')
  git clone -q --shared --no-checkout "$C/.git/modules/$sm" "$d/$sm"
  git -C "$d/$sm" checkout -q --detach "$oid"
done
echo "$d $(git -C "$d" rev-parse HEAD) pp=$(git -C "$d/protocol-processor" rev-parse HEAD) dirty=$(git -C "$d" status --porcelain | wc -l)"
