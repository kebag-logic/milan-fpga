#!/usr/bin/env bash
# clone_at.sh <sha> <dir>: a fresh clean clone of this lane at <sha>, submodules from the lane's own clones.
set -eu
L=$LANES/833-owned-process; sha=$1; d=$2
git clone -q --shared --no-checkout "$L" "$d"
git -C "$d" fetch -q "$L" "$sha"
git -C "$d" -c advice.detachedHead=false checkout -q --detach "$sha"
for dep in $(git -C "$d" config --blob "$sha:.gitmodules" --get-regexp '^submodule\..*\.path$' | cut -d' ' -f2); do
  if [ -e "$L/$dep/.git" ]; then
    git -C "$d" config "submodule.$dep.url" "$L/$dep"
    git -C "$d" -c protocol.file.allow=always submodule update -q --init --force "$dep"
  fi
done
test -z "$(git -C "$d" status --porcelain)"
