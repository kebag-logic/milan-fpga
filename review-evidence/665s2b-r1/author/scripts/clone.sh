#!/bin/bash
# A clean clone of the lane at a commit, its submodules from the lane's own checkouts (no network).
# usage: clone.sh DEST COMMIT
set -eu
L=$LANES/665-s2b-cycles
D=$1 C=$2
[ -e "$D" ] && { echo "$D exists"; exit 2; }
git clone -q --shared --no-checkout "$L" "$D"
git -C "$D" checkout -q "$C"
for s in protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis; do
    git -C "$D" config "submodule.$s.url" "$L/$s"
done
git -C "$D" -c protocol.file.allow=always submodule update -q --init $(printf ' %s' protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis)
echo "$D at $(git -C "$D" rev-parse HEAD), $(git -C "$D" status --porcelain --untracked-files=all | wc -l) changed paths"
git -C "$D" submodule status
