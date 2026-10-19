#!/usr/bin/env bash
# round 1b parent head pass: fetch the head from the lane, check it out detached in the
# submodule, clean, stage the gitlink, clean the parent's products, run the consumer gates
S=<data>/tmp/pp185-a647; P="$S/parent"; PP="$P/protocol-processor"; L=<data>/lanes/pp185-ctl
HEADSHA="$1"; R="$S/r1b/parent-head"; mkdir -p "$R"
[ "$(git -C "$PP" rev-parse --show-toplevel)" = "$PP" ] || { echo "submodule toplevel mismatch"; exit 1; }
[ "$(git -C "$P" rev-parse --show-toplevel)" = "$P" ] || { echo "parent toplevel mismatch"; exit 1; }
git -C "$PP" fetch -q "$L" 185-186-control-unlock
[ "$(git -C "$PP" rev-parse --show-toplevel)" = "$PP" ] || exit 1
git -C "$PP" checkout -q --detach "$HEADSHA"
[ "$(git -C "$PP" rev-parse --show-toplevel)" = "$PP" ] || exit 1
git -C "$PP" clean -fdXq
[ "$(git -C "$P" rev-parse --show-toplevel)" = "$P" ] || exit 1
git -C "$P" add protocol-processor
git -C "$P" clean -fdXq
git -C "$P" status --short > "$R/parent-status-before.txt"
"$S/scripts/parent_gates.sh" "$R"
