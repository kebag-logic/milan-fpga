#!/bin/bash
# A clean clone of the lane at a commit with both drafts staged in it only: lwSRP fc06e7c0 and tsn-c-stack 6532c3b0
# (their commits fetched from the round 13 drafts clone's submodules, no network), the hot list without the runtime
# entry and ctrl_arms.LWSRP_REV moved (receipts/drafts-staged.patch).
# usage: drafts.sh DEST COMMIT
set -eu
S=$MANAGEMENT/2026-09-23/665s2b-a683q/scripts
R=$MANAGEMENT/2026-09-23/665s2b-a683q/receipts
CD=$VALIDATION_STORAGE/665s2b-a683p/CD
D=$1 C=$2
$S/clone.sh "$D" "$C"
git -C "$D/third_party/lwSRP" fetch -q "$CD/third_party/lwSRP" fc06e7c0f8f7270d9c76b6f8daa666bc82d448dd
git -C "$D/third_party/lwSRP" checkout -q fc06e7c0f8f7270d9c76b6f8daa666bc82d448dd
git -C "$D/third_party/tsn-c-stack" fetch -q "$CD/third_party/tsn-c-stack" 6532c3b0f39a534be1d1f15913f97d3937b4c29b
git -C "$D/third_party/tsn-c-stack" checkout -q 6532c3b0f39a534be1d1f15913f97d3937b4c29b
git -C "$D" apply --exclude=third_party/lwSRP --exclude=third_party/tsn-c-stack "$R/drafts-staged.patch"
git -C "$D" add third_party/lwSRP third_party/tsn-c-stack
git -C "$D" status --short
