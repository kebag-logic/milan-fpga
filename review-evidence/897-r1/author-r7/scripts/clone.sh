#!/bin/bash
# A clean clone of lane 897 at a commit, its submodules from the lane's own checkouts (no network).
# usage: clone.sh DEST COMMIT
set -eu
L=$LANES/897-aspath
D=$1 C=$2
[ -e "$D" ] && { echo "$D exists"; exit 2; }
git clone -q --shared --no-checkout "$L" "$D"
git -C "$D" -c advice.detachedHead=false checkout -q "$C"
for s in $(git -C "$D" config -f .gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}' | grep -v '^external$'); do
    git -C "$D" config "submodule.$s.url" "$L/$s"
    git -C "$D" -c protocol.file.allow=always submodule update -q --init "$s"
done
echo "$D at $(git -C "$D" rev-parse HEAD), $(git -C "$D" status --porcelain --untracked-files=all | wc -l) changed paths"
git -C "$D" submodule status
