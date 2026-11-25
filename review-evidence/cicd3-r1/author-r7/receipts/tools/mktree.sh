#!/bin/bash
# mktree.sh NAME BASE [HEAD]: a --shared clone of the lane in r7/wt/NAME at BASE, with HEAD merged into it as
# GitHub's pull_request merge ref does (HEAD's tree merged into BASE); submodules from the lane's own checkouts
# (no network). Prints NAME, HEAD commit, tree, and the gptp-processor gitlink.
set -euo pipefail
LANE=/data-2/milan/lanes/cicd-1
W=/data-2/milan/tmp/cicd-a839/r7/wt/$1; BASE=$2; HEAD=${3:-}
SUBS="third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP"
[ -e "$W" ] || git clone -q --shared --no-checkout "$LANE" "$W"
git -C "$W" -c advice.detachedHead=false checkout -q -f --detach "$BASE"
if [ -n "$HEAD" ]; then
  git -C "$W" -c user.name=local -c user.email=local@invalid merge -q --no-ff --no-edit "$HEAD" \
    -m "Merge $(git -C "$W" rev-parse "$HEAD") into $(git -C "$W" rev-parse "$BASE")"
fi
for d in $SUBS; do git -C "$W" config "submodule.$d.url" "$LANE/$d"; done
git -C "$W" -c protocol.file.allow=always submodule update -q --init --force $SUBS
for d in $SUBS; do git -C "$W/$d" remote set-url origin "$(git -C "$W" config -f .gitmodules "submodule.$d.url")"; done
echo "$1 $(git -C "$W" rev-parse HEAD) tree $(git -C "$W" rev-parse HEAD^{tree}) gptp-processor $(git -C "$W" rev-parse HEAD:gptp-processor)"
