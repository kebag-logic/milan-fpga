#!/usr/bin/env bash
# chain1.sh: the shipping AX7101 1x1 TDM8 route set at the route commit, the resource gate's recipe form
# (docs/testing/PP_SHADOW_BASELINE_RECIPE.md): export, route-1x1 at ExtraPostPlacementOpt with its single-thread
# synthesis, its worst paths, then AltSpreadLogic_high and ExtraTimingOpt from the same synthesis checkpoint, each
# with its worst paths. One Vivado run at a time, each through the slot wrapper in its own scope (MemoryMax 14G).
# Stops at the first failed step. Writes $L/chain1.rc at the end.
set -u
here=$(cd "$(dirname "$0")" && pwd)
V=<scratch>/viv; W=$V/w; R=$V/gclone; L=$V/logs
M=<mgmt>/2026-09-23
stamp() { echo "== $1 $(date -u +%FT%TZ)"; }
fail() { echo "$1"; echo 1 > "$L/chain1.rc"; exit 1; }
viv() { # name dir script
  stamp "SLOT-WAIT $1"
  bash "$M/vivado-slot.sh" systemd-run --user --scope --quiet --unit="milan-883-a768-viv-$1-$$" -p MemoryMax=14G \
    bash "$here/viv.sh" "$2" "$3" > "$L/$1.slot.log" 2>&1
  rc=$?; stamp "DONE $1 rc=$rc"; [ "$rc" = 0 ] || fail "$1 FAILED rc=$rc"
}
paths() { # name routed-dir
  stamp "PATHS $1"
  bash "$here/paths.sh" "$2/alinx_ax7101_route.dcp" "$V/paths/$1" "$R" > "$L/paths-$1.log" 2>&1
  stamp "PATHS-DONE $1 rc=$?"
}
mkdir -p "$L"; rm -f "$L/chain1.rc"
stamp EXPORT
bash "$here/export_shape.sh" ax7101 "$W" "$R" > "$L/export.log" 2>&1 || fail "EXPORT FAILED rc=$?"
source "$here/env.sh"
export PATH="<litex>/venv/bin:$PATH"
( cd "$R" && python3 syn/ooc/pp_baseline.py "$W/ax7101/gateware" --single-thread-synthesis ) > "$L/prep-1x1.log" 2>&1 || fail "PREP FAILED"
viv eppo "$W/ax7101/gateware" baseline_integrated.tcl
python3 -B "$here/dir_prep.py" "$R" "$W" > "$L/dir-prep.log" 2>&1 || fail "DIR-PREP FAILED"
viv aslh "$W/ax7101-AltSpreadLogic_high" baseline_implementation.tcl
viv eto "$W/ax7101-ExtraTimingOpt" baseline_implementation.tcl
paths eppo "$W/ax7101/gateware"
paths aslh "$W/ax7101-AltSpreadLogic_high"
paths eto "$W/ax7101-ExtraTimingOpt"
stamp CHAIN-COMPLETE
echo 0 > "$L/chain1.rc"
