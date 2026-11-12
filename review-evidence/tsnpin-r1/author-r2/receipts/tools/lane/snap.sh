#!/usr/bin/env bash
# snap.sh <dir> [sha]: a clean shared clone of the lane at <sha> (default: a stash-create snapshot of the working tree) with its submodules.
set -eu
L=<lane>; d=$1; sha=${2:-}
if [ -z "$sha" ]; then sha=$(git -C "$L" stash create); [ -n "$sha" ] || sha=$(git -C "$L" rev-parse HEAD); fi
rm -rf "$d"
git clone -q --shared --no-checkout "$L" "$d"
git -C "$d" -c advice.detachedHead=false checkout -q --detach "$sha"
git -C "$d" remote set-url origin https://github.com/kebag-logic/milan-fpga.git
for dep in $(git -C "$d" config --file .gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}'); do
  if [ -e "$L/$dep/.git" ]; then
    git -C "$d" config "submodule.$dep.url" "$L/$dep"
    git -C "$d" -c protocol.file.allow=always submodule update -q --init --force "$dep"
  fi
done
test -z "$(git -C "$d" status --porcelain)"
echo "$sha"
