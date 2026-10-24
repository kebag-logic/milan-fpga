#!/usr/bin/env bash
# A clean clone of the lane at one revision, its initialised submodules taken
# from the lane's own checkouts (no network), for a campaign, a route or a gate.
# usage: make_clone.sh <dest> <rev>
set -euo pipefail
lane=$LANES/773-aaf-lead
dest=$1; rev=$2
test ! -e "$dest"
git clone -q --no-checkout "$lane" "$dest"
git -C "$dest" checkout -q --detach "$rev"
for sm in $(git -C "$dest" config -f .gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}'); do
  [ "$sm" = external ] && continue
  git -C "$dest" config "submodule.$sm.url" "$lane/$sm"
  git -C "$dest" -c protocol.file.allow=always submodule update -q --init "$sm"
done
git -C "$dest" rev-parse HEAD
git -C "$dest" submodule status
git -C "$dest" status --short | head
