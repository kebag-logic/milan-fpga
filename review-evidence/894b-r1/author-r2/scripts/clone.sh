#!/bin/bash
# A clean clone of the lane at a commit, its submodules from the lane's own checkouts (no network).
# usage: clone.sh DEST COMMIT
set -eu
L=/data-2/milan/lanes/894-8x8
D=$1 C=$2
[ -e "$D" ] && { echo "$D exists"; exit 2; }
test "$(git -C "$L/protocol-processor" rev-parse --show-toplevel)" = "$L/protocol-processor"
git -C "$L/protocol-processor" remote get-url origin | grep -q 'protocol-processor-control-plane-avb-milan'
git clone -q --shared --no-checkout "$L" "$D"
git -C "$D" -c advice.detachedHead=false checkout -q "$C"
for s in protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis external; do
    git -C "$D" config "submodule.$s.url" "$L/$s"
done
git -C "$D" -c protocol.file.allow=always submodule update -q --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
echo "$D at $(git -C "$D" rev-parse HEAD), $(git -C "$D" status --porcelain --untracked-files=all | wc -l) changed paths"
git -C "$D" submodule status
