#!/usr/bin/env bash
# clone_probe.sh SRC DEST: a disposable clone of SRC at SRC's HEAD, every initialised submodule at its gitlink.
set -eu
src=$1; d=$2
test ! -e "$d"
git clone -q --shared --no-checkout "$src" "$d"
git -C "$d" -c advice.detachedHead=false checkout -q --detach "$(git -C "$src" rev-parse HEAD)"
for dep in $(git -C "$d" config --blob HEAD:.gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}'); do
  [ -e "$src/$dep/.git" ] || { echo "skip $dep (not initialised in source)"; continue; }
  git -C "$d" config "submodule.$dep.url" "$src/$dep"
  git -C "$d" -c protocol.file.allow=always submodule update -q --init --force "$dep"
done
git -C "$d" status --porcelain --untracked-files=all --ignore-submodules=none | wc -l
git -C "$d" rev-parse HEAD
