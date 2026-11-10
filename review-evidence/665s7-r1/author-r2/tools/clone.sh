#!/usr/bin/env bash
# clone.sh <dir> <head>: a clean clone of the lane at <head>, every submodule from the lane's own clone of it
set -euo pipefail
DIR=$1; HEAD=$2; SRC=$LANES/665-s7-srp-tx
[ -e "$DIR" ] && { echo "exists: $DIR" >&2; exit 2; }
git clone -q --shared --no-checkout "$SRC" "$DIR"
cd "$DIR"
git fetch -q "$SRC" "+refs/heads/*:refs/remotes/lane/*"
git -c advice.detachedHead=false checkout -q -f --detach "$HEAD"
for dep in $(git config --blob "$HEAD:.gitmodules" --get-regexp '^submodule\..*\.path$' | awk '{print $2}' | grep -vx external); do
  if [ -e "$SRC/$dep/.git" ]; then git config "submodule.$dep.url" "$SRC/$dep"; fi
  git -c protocol.file.allow=always submodule update -q --init --force "$dep"
done
test -z "$(git status --porcelain)"
git rev-parse HEAD
