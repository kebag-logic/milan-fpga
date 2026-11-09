#!/usr/bin/env bash
# chain1.sh: the shipping AX7101 1x1 route set and ooc-1x1 at the lane head, in the resource gate's recipe form
# (docs/testing/PP_SHADOW_BASELINE_RECIPE.md, Integrated, Standalone and Resource gate): the export, route-1x1 at
# ExtraPostPlacementOpt with its single-thread synthesis; once that run has written its synthesis checkpoint, the
# two comparison directives (AltSpreadLogic_high, ExtraTimingOpt) placed from that checkpoint and ooc-1x1 from its
# synthesis log, in parallel (round 2 ruling: up to three Vivado runs at once). Every Vivado run goes through the
# slot wrapper in its own scope (MemoryMax 14G), inheriting this unit's CPUs. After each route, its worst setup and
# hold paths by report_timing (paths.sh, read-only). Stops at the first failed step; the gate runs afterwards.
set -u
here=$(cd "$(dirname "$0")" && pwd)
S=$VALIDATION_STORAGE/scratch/854-a756b; W=$S/w; R=$S/aclone; L=$S/alogs
M=$HOME/milan-fpga-management/2026-09-23
stamp() { echo "== $1 $(date -u +%FT%TZ)"; }
viv() { # name dir script
  stamp "SLOT-WAIT $1"
  bash "$M/vivado-slot.sh" systemd-run --user --scope --quiet --unit="milan-854-a756b-viv-$1-$$" -p MemoryMax=14G \
    bash "$here/viv.sh" "$2" "$3" > "$L/$1.slot.log" 2>&1
  rc=$?; stamp "DONE $1 rc=$rc"; echo "$rc" > "$L/$1.rc"; return $rc
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
( viv eppo "$W/ax7101/gateware" baseline_integrated.tcl && paths eppo "$W/ax7101/gateware" ) &
stamp WAIT-SYNTH-CHECKPOINT
until [ -f "$W/ax7101/gateware/baseline.log" ] && grep -q "Command: opt_design" "$W/ax7101/gateware/baseline.log"; do
  [ -f "$L/eppo.rc" ] && { echo "eppo ended before opt_design"; wait; exit 1; }
  sleep 30
done
stamp SYNTH-CHECKPOINT-WRITTEN
python3 -B "$here/dir_prep.py" "$R" "$W" > "$L/dir-prep.log" 2>&1 || { echo DIR-PREP FAILED; wait; exit 1; }
( cd "$R" && python3 syn/ooc/pp_baseline.py "$W/ax7101/gateware" --single-thread-synthesis --output "$W/ax7101-ooc" \
    --integrated-log "$W/ax7101/gateware/baseline.log" --integrated-clock ) > "$L/ooc-prep.log" 2>&1 || { echo OOC-PREP FAILED; wait; exit 1; }
( viv aslh "$W/ax7101-AltSpreadLogic_high" baseline_implementation.tcl && paths aslh "$W/ax7101-AltSpreadLogic_high" ) &
sleep 60
( viv eto "$W/ax7101-ExtraTimingOpt" baseline_implementation.tcl && paths eto "$W/ax7101-ExtraTimingOpt" ) &
sleep 60
viv ooc "$W/ax7101-ooc" baseline_ooc.tcl &
wait
for n in eppo aslh eto ooc; do echo "$n rc=$(cat "$L/$n.rc" 2>/dev/null || echo missing)"; done
stamp CHAIN-COMPLETE
