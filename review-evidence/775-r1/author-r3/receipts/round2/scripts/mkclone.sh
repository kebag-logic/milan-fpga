#!/bin/bash
# mkclone.sh <dest> <rev>: a --shared clone of the lane at <rev>, with the
# submodules the tree's .gitmodules lists (bar 'external') from the lane's own
# submodule checkouts; refuses a dirty result
set -e
src=<lane>
dest=$1; rev=$2
[ -e "$dest" ] || git clone -q --shared --no-checkout "$src" "$dest"
cd "$dest"
git fetch -q "$src" "$rev"
git -c advice.detachedHead=false checkout -q -f --detach "$rev"
deps=$(git config -f .gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}' | grep -vx external)
git clean -q -fdx $(for d in $deps; do printf -- '-e %s ' "$d"; done)
for d in $deps; do
  if [ -e "$src/$d/.git" ]; then git config "submodule.$d.url" "$src/$d"; fi
done
git -c protocol.file.allow=always submodule update -q --init --force $deps
test -z "$(git status --porcelain --untracked-files=no)"
echo "clone $dest at $(git rev-parse HEAD)"
git submodule status
