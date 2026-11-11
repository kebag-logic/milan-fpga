#!/usr/bin/env bash
# devsync.sh: the dev clone at the lane's HEAD with the lane's uncommitted changes applied (iteration only, never a gate)
set -euo pipefail
L=<lane>; D=<scratch>/dev
H=$(git -C $L rev-parse HEAD)
[ -d $D ] || bash <scratch>/tools/clone.sh $D $H >/dev/null
git -C $D fetch -q $L "+HEAD:refs/remotes/lane/head"
git -C $D checkout -q -f --detach "$H"
git -C $D clean -q -fd -e 'obj*' -e '*/obj*'
git -C $L diff HEAD --binary | git -C $D apply --allow-empty
for f in $(git -C $L ls-files --others --exclude-standard); do mkdir -p "$D/$(dirname $f)"; cp -p "$L/$f" "$D/$f"; done
echo "dev at $H + $(git -C $L diff HEAD --stat | tail -1)"
