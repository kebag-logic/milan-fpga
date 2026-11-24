#!/usr/bin/env bash
# clone.sh <rev> <dir>: a clean --shared clone of this lane at <rev>, submodules (all but `external`) from the lane's checkouts.
set -euo pipefail
LANE=/data-2/milan/lanes/opt-gptp-sw; rev=$1; dir=$2
[ -e "$dir" ] && { echo "$dir exists" >&2; exit 2; }
git clone -q --shared --no-checkout "$LANE" "$dir"
git -C "$dir" -c advice.detachedHead=false checkout -q --detach "$rev"
git -C "$dir" remote set-url origin https://github.com/kebag-logic/milan-fpga.git
for dep in $(git -C "$dir" config -f .gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}'); do
  [ "$dep" = external ] && continue
  git -C "$dir" config "submodule.$dep.url" "$LANE/$dep"
done
deps=$(git -C "$dir" config -f .gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}' | grep -v '^external$')
git -C "$dir" -c protocol.file.allow=always submodule update -q --init --force $deps
git -C "$dir" submodule status
echo "head $(git -C "$dir" rev-parse HEAD) porcelain $(git -C "$dir" status --porcelain --untracked-files=all | wc -l)"
