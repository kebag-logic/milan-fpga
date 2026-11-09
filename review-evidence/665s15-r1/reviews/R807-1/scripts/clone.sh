#!/bin/bash
# Clean clone of the review clone at COMMIT, submodules from the review clone's checkouts (no network).
# usage: clone.sh SRC DEST COMMIT
set -eu
L=$1 D=$2 C=$3
[ -e "$D" ] && { echo "$D exists"; exit 2; }
git clone -q --shared --no-checkout "$L" "$D"
git -C "$D" checkout -q "$C"
for s in protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis; do
    git -C "$D" config "submodule.$s.url" "$L/$s"
done
git -C "$D" -c protocol.file.allow=always submodule update -q --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
echo "$D at $(git -C "$D" rev-parse HEAD), $(git -C "$D" status --porcelain --untracked-files=all | wc -l) changed paths"
git -C "$D" submodule status
