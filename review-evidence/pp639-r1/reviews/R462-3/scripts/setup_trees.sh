#!/bin/sh
# Extract disposable trees for the R462-3 probes. Usage: setup_trees.sh REPO PACKET
# head      : exact head c725be1
# mainrtl   : head tree with main b0a7419's top and listener RTL (the lane's two
#             HDL files reverted), so the head's benches grade main's RTL
set -eu
REPO=$1; PKT=$2; S=$PKT/scratch
HEAD=c725be12d7ea6bf96f1b64e3a56416f0d4defd6c
MAIN=b0a74196
rm -rf "$S/head" "$S/mainrtl"; mkdir -p "$S/head" "$S/mainrtl"
git -C "$REPO" archive "$HEAD" | tar -x -C "$S/head"
git -C "$REPO" archive "$HEAD" | tar -x -C "$S/mainrtl"
for f in hdl/top/protocol_processor_top.sv hdl/acmp/KL_pp_acmp_listener.sv; do
  git -C "$REPO" show "$MAIN:$f" > "$S/mainrtl/$f"
done
# the mainrtl tree differs from main only in tb/ and docs/ (the lane's tests)
git -C "$REPO" diff --stat "$MAIN" "$HEAD" -- hdl/
