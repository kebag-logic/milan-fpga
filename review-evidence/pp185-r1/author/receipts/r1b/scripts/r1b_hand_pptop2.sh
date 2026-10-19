#!/usr/bin/env bash
# round 1b hand-planted mutant, continued: the same plant, the line build's AX and the
# sixth (timer-defaults) build; then the tree is restored and checked clean
S=<data>/tmp/pp185-a647; L=<data>/lanes/pp185-ctl; R="$S/r1b/hand"; mkdir -p "$R"
[ "$(git -C "$L" rev-parse --show-toplevel)" = "$L" ] || exit 1
sed -i "s/          lockf_r   <= LOCKF_UNLOCK_C;/          lockf_r   <= 32'd0;/" "$L/hdl/aecp/KL_aecp_notify.sv"
git -C "$L" diff > "$R/pptop2-timeout-zero-planted.patch"
"$S/scripts/gate.sh" "$R" pptop-line-timeout-zero-planted "$L/tb/pp_top" make aecp-line
"$S/scripts/gate.sh" "$R" pptop-timerdef-timeout-zero-planted "$L/tb/pp_top" make timer-defaults
git -C "$L" checkout -- hdl/aecp/KL_aecp_notify.sv
git -C "$L" status --short > "$R/pptop2-status-after-restore.txt"
echo done > "$R/pptop2.done"
