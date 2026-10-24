#!/usr/bin/env bash
# A clean clone of <src> at <rev>, its submodules taken from <src>'s own checkouts (no network; `external` skipped).
# usage: make_clone.sh <src> <dest> <rev>
set -euo pipefail
src=$1; dest=$2; rev=$3
test ! -e "$dest"
git clone -q --no-checkout "$src" "$dest"
git -C "$dest" checkout -q --detach "$rev"
for sm in $(git -C "$dest" config -f .gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}'); do
  [ "$sm" = external ] && continue
  git -C "$dest" config "submodule.$sm.url" "$src/$sm"
  git -C "$dest" -c protocol.file.allow=always submodule update -q --init "$sm"
done
echo "head $(git -C "$dest" rev-parse HEAD) tree $(git -C "$dest" rev-parse 'HEAD^{tree}')"
git -C "$dest" submodule status
echo "tracked changes: $(git -C "$dest" status --porcelain --untracked-files=no | wc -l)"
