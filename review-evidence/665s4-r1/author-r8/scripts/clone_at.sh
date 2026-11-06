#!/usr/bin/env bash
# clone_at.sh <sha> <dir>: a fresh clean clone of the lane at <sha>, every submodule at its gitlink from the
# lane's own clone of it (round 5 runs every gate on such a clone of the committed head).
set -eu
L=$LANES/665-s4-f1-target; sha=$1; d=$2
test ! -e "$d"
git clone -q --shared --no-checkout "$L" "$d"
git -C "$d" fetch -q "$L" "$sha"
git -C "$d" -c advice.detachedHead=false checkout -q --detach "$sha"
git -C "$d" remote set-url origin https://github.com/kebag-logic/milan-fpga.git
for dep in $(git -C "$d" config --blob "$sha:.gitmodules" --get-regexp '^submodule\..*\.path$' | awk '{print $2}'); do
  git -C "$d" config "submodule.$dep.url" "$L/$dep"
  git -C "$d" -c protocol.file.allow=always submodule update -q --init --force "$dep"
  test "$(git -C "$d/$dep" rev-parse --show-toplevel)" = "$d/$dep"
  git -C "$d/$dep" remote get-url origin
done
test "$(git -C "$d" rev-parse HEAD)" = "$(git -C "$L" rev-parse "$sha")"
test -z "$(git -C "$d" status --porcelain --untracked-files=all --ignore-submodules=none)"
git -C "$d" submodule status
