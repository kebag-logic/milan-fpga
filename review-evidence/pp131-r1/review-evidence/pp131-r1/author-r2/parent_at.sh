#!/bin/sh
# Point the scratch parent's protocol-processor at the lane: `head` = the lane's
# committed branch head; `wt` = a scratch-only commit of the lane's working tree.
set -e
P=$VALIDATION_STORAGE/a425/parent
S=$P/protocol-processor
L=$LANES/pp131-d3-core
cd "$S"
git fetch -q "$L" 131-d3-core-scalars
git checkout -q -f FETCH_HEAD
git clean -q -fdx
if [ "$1" = wt ]; then
  (cd "$L" && git ls-files -co --exclude-standard | tar -cf - -T -) | tar -xf -
  git add -A
  git -c user.name=scratch -c user.email=scratch@invalid commit -q -m "scratch snapshot of the working tree" || true
fi
cd "$P"
git add protocol-processor
echo "protocol-processor at $(git -C "$S" rev-parse HEAD)"
