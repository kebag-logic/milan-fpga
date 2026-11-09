#!/usr/bin/env bash
# make_clone.sh <dest> <rev>: a clean clone of the lane at <rev>, its submodules from the lane's own checkouts (no network).
set -euo pipefail
lane=$LANES/854-shadow-drops; dest=$1; rev=$2
test ! -e "$dest"
git clone -q --no-checkout "$lane" "$dest"
git -C "$dest" -c advice.detachedHead=false checkout -q --detach "$rev"
test "$(git -C "$dest" rev-parse HEAD)" = "$(git -C "$lane" rev-parse "$rev^{commit}")"
for sm in $(git -C "$dest" config --blob "$rev:.gitmodules" --get-regexp '^submodule\..*\.path$' | awk '{print $2}'); do
  if [ -e "$lane/$sm/.git" ]; then
    git -C "$dest" config "submodule.$sm.url" "$lane/$sm"
    git -C "$dest" -c protocol.file.allow=always submodule update -q --init "$sm"
  fi
done
git -C "$dest" remote set-url origin https://github.com/kebag-logic/milan-fpga.git
test -z "$(git -C "$dest" status --porcelain)"
git -C "$dest" rev-parse HEAD; git -C "$dest" submodule status
