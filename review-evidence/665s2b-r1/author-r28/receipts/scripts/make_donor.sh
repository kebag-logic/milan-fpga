#!/bin/bash
# A scratch copy of a measurement clone with the tsn-c-stack#32 donor applied at the lane's pin, committed in its
# submodule and gitlinked, so the image builds it as the pinned stack. usage: make_donor.sh SRC DST
set -eu
S=$1 D=$2 L=<lane>
[ -e "$D" ] && { echo "$D exists"; exit 2; }
git clone -q --shared --no-checkout "$S" "$D"
git -C "$D" checkout -q "$(git -C "$S" rev-parse HEAD)"
for s in protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis; do
    git -C "$D" config "submodule.$s.url" "$L/$s"
done
git -C "$D" -c protocol.file.allow=always submodule update -q --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
git -C "$D/third_party/tsn-c-stack" apply --3way <scratch>/donor-core.patch
git -C "$D/third_party/tsn-c-stack" -c user.name=scratch -c user.email=scratch@invalid commit -q -m "scratch: tsn-c-stack#32 donor at the pin"
git -C "$D" add third_party/tsn-c-stack
git -C "$D" -c user.name=scratch -c user.email=scratch@invalid commit -q -m "scratch: the stack with the tsn-c-stack#32 donor"
echo "$D at $(git -C "$D" rev-parse HEAD); stack $(git -C "$D/third_party/tsn-c-stack" rev-parse HEAD); $(git -C "$D" status --porcelain | wc -l) changed"
