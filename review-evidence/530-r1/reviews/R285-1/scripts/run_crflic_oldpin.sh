#!/usr/bin/env bash
# The #530 item 1 failing arm: build and run obj_crflic with the protocol
# processor checked out at its previous pin, then restore the recorded pin.
# usage: run_crflic_oldpin.sh <repo> <verilator>
set -uo pipefail
repo=$1; ver=$2
old=424c688fa2205b934a7689a58f2aa766420f2326
pin=$(git -C "$repo" rev-parse :protocol-processor)
git -C "$repo/protocol-processor" checkout -q "$old" || exit 2
echo "processor checkout $(git -C "$repo/protocol-processor" rev-parse HEAD)"
"$(dirname "$0")/run_crflic.sh" "$repo" "$ver" obj_crflic_oldpin
rc=$?
git -C "$repo/protocol-processor" checkout -q "$pin"
echo "processor restored to $(git -C "$repo/protocol-processor" rev-parse HEAD) (pin $pin)"
exit $rc
