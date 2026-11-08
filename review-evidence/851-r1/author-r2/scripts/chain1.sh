#!/usr/bin/env bash
# chain1.sh: the shipping AX7101 1x1 TDM8 route set at the merge commit, in the resource gate's recipe form
# (docs/testing/PP_SHADOW_BASELINE_RECIPE.md, Resource gate): the export, route-1x1 at ExtraPostPlacementOpt with its
# single-thread synthesis, ooc-1x1 (synthesis only), then AltSpreadLogic_high and ExtraTimingOpt placed from the same
# synthesis checkpoint. One Vivado run at a time, each through the slot wrapper in its own scope (MemoryMax 14G),
# inheriting this unit's CPUs. After each route, its worst setup and hold paths by report_timing (paths.sh), beside
# the next run (a read-only timing report, not a route).
# Stops at the first failed step; the gate itself runs afterwards.
set -u
here=$(cd "$(dirname "$0")" && pwd)
S=$VALIDATION_STORAGE/scratch/851-a744b; W=$S/w; R=$S/gclone; L=$S/glogs
M=$HOME/milan-fpga-management/2026-09-23
stamp() { echo "== $1 $(date -u +%FT%TZ)"; }
viv() { # name dir script
  stamp "SLOT-WAIT $1"
  bash "$M/vivado-slot.sh" systemd-run --user --scope --quiet --unit="milan-851-a744b-viv-$1-$$" -p MemoryMax=14G \
    bash "$here/viv.sh" "$2" "$3" > "$L/$1.slot.log" 2>&1
  rc=$?; stamp "DONE $1 rc=$rc"; [ "$rc" = 0 ] || { echo "$1 FAILED rc=$rc"; exit 1; }
}
paths() { # name routed-dir
  stamp "PATHS $1"
  bash "$here/paths.sh" "$2/alinx_ax7101_route.dcp" "$S/paths/$1" > "$L/paths-$1.log" 2>&1
  stamp "PATHS-DONE $1 rc=$?"
}
mkdir -p "$L"
stamp EXPORT
bash "$here/export_shape.sh" ax7101 "$W" > "$L/export.log" 2>&1 || { echo "EXPORT FAILED rc=$?"; exit 1; }
source "$here/env.sh"
export PATH="$HOME/litex-milan/venv/bin:$PATH"
( cd "$R" && python3 syn/ooc/pp_baseline.py "$W/ax7101/gateware" --single-thread-synthesis ) > "$L/prep-1x1.log" 2>&1 || { echo PREP FAILED; exit 1; }
viv eppo "$W/ax7101/gateware" baseline_integrated.tcl
paths eppo "$W/ax7101/gateware" &
stamp OOC-PREP
( cd "$R" && python3 syn/ooc/pp_baseline.py "$W/ax7101/gateware" --single-thread-synthesis --output "$W/ax7101-ooc" \
    --integrated-log "$W/ax7101/gateware/baseline.log" --integrated-clock ) > "$L/ooc-prep.log" 2>&1 || { echo OOC-PREP FAILED; exit 1; }
viv ooc "$W/ax7101-ooc" baseline_ooc.tcl
python3 -B "$here/dir_prep.py" "$R" "$W" > "$L/dir-prep.log" 2>&1 || { echo DIR-PREP FAILED; exit 1; }
viv aslh "$W/ax7101-AltSpreadLogic_high" baseline_implementation.tcl
paths aslh "$W/ax7101-AltSpreadLogic_high" &
viv eto "$W/ax7101-ExtraTimingOpt" baseline_implementation.tcl
paths eto "$W/ax7101-ExtraTimingOpt" &
wait
stamp CHAIN-COMPLETE
