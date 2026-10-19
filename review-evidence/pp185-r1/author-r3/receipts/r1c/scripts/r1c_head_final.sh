#!/usr/bin/env bash
# round 1c final head: after the head campaigns, clean the lane's ignored products and run
# every processor gate at the final head
S=$VALIDATION_STORAGE/pp185-a647; L=$LANES/pp185-ctl
while [ ! -e "$S/r1c/head/stream-big.done" ]; do timeout 30 tail -f /dev/null; done
[ "$(git -C "$L" rev-parse --show-toplevel)" = "$L" ] || { echo "toplevel mismatch"; exit 1; }
git -C "$L" clean -fdXq
"$S/scripts/proc_gates.sh" "$L" "$S/r1c/head-final/gates"
echo ALL-DONE > "$S/r1c/head-final/done"
