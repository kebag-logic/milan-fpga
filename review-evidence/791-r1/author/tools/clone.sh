#!/usr/bin/env bash
# clone.sh <dir> <head>: a clean clone of the lane at <head>, every submodule but external from the lane's own clone.
set -euo pipefail
DIR=$1; HEAD=$2; SRC=$LANES/791-region-decode
[ -e "$DIR" ] && { echo "exists: $DIR" >&2; exit 2; }
git clone -q --shared --no-checkout "$SRC" "$DIR"
cd "$DIR"
git -c advice.detachedHead=false checkout -q -f --detach "$HEAD"
for dep in $(git config --blob "$HEAD:.gitmodules" --get-regexp '^submodule\..*\.path$' | awk '{print $2}' | grep -vx external); do
  [ "$(git -C "$SRC/$dep" rev-parse --show-toplevel)" = "$SRC/$dep" ] || { echo "not a repository: $SRC/$dep" >&2; exit 2; }
  git config "submodule.$dep.url" "$SRC/$dep"
  git -c protocol.file.allow=always submodule update -q --init --force "$dep"
done
test -z "$(git status --porcelain)"
git rev-parse HEAD
