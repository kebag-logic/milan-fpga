#!/usr/bin/env bash
# round 2 parent head pass: after the base pass, check the head out detached in the
# submodule, commit the gitlink in the local scratch parent (never pushed), run the pass
S=$VALIDATION_STORAGE/pp185-a647; P="$S/parent"; PP="$P/protocol-processor"
HEADSHA="$1"
while [ ! -e "$S/r2/rec/parent-base/parent.done" ]; do timeout 30 tail -f /dev/null; done
[ "$(git -C "$PP" rev-parse --show-toplevel)" = "$PP" ] || { echo "submodule toplevel mismatch"; exit 1; }
git -C "$PP" fetch -q $LANES/pp185-ctl 185-186-control-unlock:refs/remotes/lane/185-186-control-unlock || exit 1
[ "$(git -C "$PP" rev-parse --show-toplevel)" = "$PP" ] || exit 1
git -C "$PP" checkout -q --detach "$HEADSHA" || exit 1
[ "$(git -C "$P" rev-parse --show-toplevel)" = "$P" ] || { echo "parent toplevel mismatch"; exit 1; }
git -C "$P" add protocol-processor || exit 1
git -C "$P" commit -q -m "Scratch: protocol-processor at round-2 head ${HEADSHA:0:8}" || exit 1
"$S/scripts/r2_parent.sh" head "$HEADSHA" "$S/r2/rec/parent-base/parent.done"
