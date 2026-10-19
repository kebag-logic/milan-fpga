#!/usr/bin/env bash
# round 1b hand-planted mutant: both timeout latches back to 0 (the round-1 head), the
# whole tb/pp_top suite, unpiped; then the tree is restored and checked clean
S=$VALIDATION_STORAGE/pp185-a647; L=$LANES/pp185-ctl; R="$S/r1b/hand"; mkdir -p "$R"
[ "$(git -C "$L" rev-parse --show-toplevel)" = "$L" ] || exit 1
sed -i "s/          lockf_r   <= LOCKF_UNLOCK_C;/          lockf_r   <= 32'd0;/" "$L/hdl/aecp/KL_aecp_notify.sv"
git -C "$L" diff > "$R/pptop-timeout-zero-planted.patch"
"$S/scripts/gate.sh" "$R" pptop-timeout-zero-planted "$L/tb/pp_top" make -k
git -C "$L" checkout -- hdl/aecp/KL_aecp_notify.sv
git -C "$L" status --short > "$R/pptop-status-after-restore.txt"
echo done > "$R/pptop.done"
