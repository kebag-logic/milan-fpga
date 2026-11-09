#!/usr/bin/env bash
# route1.sh: the shipping AX7101 1x1 route at the lane head in the resource gate's recipe form
# (docs/testing/PP_SHADOW_BASELINE_RECIPE.md): the export, then route-1x1 at the shipping directive
# ExtraPostPlacementOpt with its single-thread synthesis, through the slot wrapper in its own scope (MemoryMax 12G).
# One directive only (assignment); no comparison routes. Stops at the first failed step.
set -u
here=$(cd "$(dirname "$0")" && pwd)
S=$VALIDATION_STORAGE/scratch/854-a756; W=$S/w; R=$S/rclone; L=$S/rlogs
M=$HOME/milan-fpga-management/2026-09-23
stamp() { echo "== $1 $(date -u +%FT%TZ)"; }
mkdir -p "$L"
stamp EXPORT
bash "$here/export_shape.sh" ax7101 "$W" > "$L/export.log" 2>&1 || { echo "EXPORT FAILED rc=$?"; exit 1; }
source "$here/env.sh"
export PATH="$HOME/litex-milan/venv/bin:$PATH"
( cd "$R" && python3 syn/ooc/pp_baseline.py "$W/ax7101/gateware" --single-thread-synthesis ) > "$L/prep-1x1.log" 2>&1 || { echo PREP FAILED; exit 1; }
stamp SLOT-WAIT
bash "$M/vivado-slot.sh" systemd-run --user --scope --quiet --unit="milan-854-a756-viv-eppo-$$" -p MemoryMax=12G \
  bash "$here/viv.sh" "$W/ax7101/gateware" baseline_integrated.tcl > "$L/eppo.slot.log" 2>&1
rc=$?; stamp "DONE eppo rc=$rc"; [ "$rc" = 0 ] || { echo "eppo FAILED rc=$rc"; exit 1; }
stamp CHAIN-COMPLETE
