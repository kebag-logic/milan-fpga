#!/usr/bin/env bash
# usage: clone_at.sh <source checkout> <sha> <dir>
# A fresh clean shared clone of <source checkout> at <sha>, with each submodule
# taken from the source checkout's own submodule repositories. Writes only <dir>.
set -eu
src=$1; sha=$2; d=$3
git clone -q --shared --no-checkout "$src" "$d"
git -C "$d" -c advice.detachedHead=false checkout -q --detach "$sha"
for dep in $(git -C "$d" config --blob "$sha:.gitmodules" --get-regexp '^submodule\..*\.path$' | cut -d' ' -f2); do
  if [ -e "$src/$dep/.git" ]; then
    git -C "$d" config "submodule.$dep.url" "$src/$dep"
    git -C "$d" -c protocol.file.allow=always submodule update -q --init --force "$dep"
  fi
done
test "$(git -C "$d" rev-parse HEAD)" = "$sha"
test -z "$(git -C "$d" status --porcelain)"
