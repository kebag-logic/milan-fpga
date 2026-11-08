#!/usr/bin/env bash
# chain1.sh: the resource gate's 1x1 measurement set in the gate clone, one Vivado run at a time through the slot
# wrapper: route-1x1 at the shipping directive, ooc-1x1, then the two comparison directives. Each run sits in its own
# scope (MemoryMax 14G) and inherits this unit's CPUs. Stops at the first failed step; the gate itself runs afterwards.
set -u
here=$(cd "$(dirname "$0")" && pwd)
S=$VALIDATION_STORAGE/scratch/851-a744; W=$S/w; R=$S/gclone; L=$S/glogs
M=$HOME/milan-fpga-management/2026-09-23
stamp() { echo "== $1 $(date -u +%FT%TZ)"; }
viv() { # name dir script
  stamp "SLOT-WAIT $1"
  bash "$M/vivado-slot.sh" systemd-run --user --scope --quiet --unit="milan-851-a744-viv-$1-$$" -p MemoryMax=14G \
    bash "$here/viv.sh" "$2" "$3" > "$L/$1.slot.log" 2>&1
  rc=$?; stamp "DONE $1 rc=$rc"; [ "$rc" = 0 ] || { echo "$1 FAILED rc=$rc"; exit 1; }
}
mkdir -p "$L"
stamp EXPORT
bash "$here/export_shape.sh" ax7101 "$W" > "$L/export.log" 2>&1 || { echo "EXPORT FAILED rc=$?"; exit 1; }
source "$here/env.sh"
export PATH="$HOME/litex-milan/venv/bin:$PATH"
( cd "$R" && python3 syn/ooc/pp_baseline.py "$W/ax7101/gateware" --single-thread-synthesis ) > "$L/prep-1x1.log" 2>&1 || { echo PREP FAILED; exit 1; }
# one route at a time: the shipping route at the same head must have finished first
stamp WAIT-SHIPPING-ROUTE
until [ -f "$S/route-a566d4f9/build.rc" ]; do sleep 30; done
viv eppo "$W/ax7101/gateware" baseline_integrated.tcl
stamp OOC-PREP
( cd "$R" && python3 syn/ooc/pp_baseline.py "$W/ax7101/gateware" --single-thread-synthesis --output "$W/ax7101-ooc" \
    --integrated-log "$W/ax7101/gateware/baseline.log" --integrated-clock ) > "$L/ooc-prep.log" 2>&1 || { echo OOC-PREP FAILED; exit 1; }
viv ooc "$W/ax7101-ooc" baseline_ooc.tcl
python3 -B "$here/dir_prep.py" "$R" "$W" > "$L/dir-prep.log" 2>&1 || { echo DIR-PREP FAILED; exit 1; }
viv aslh "$W/ax7101-AltSpreadLogic_high" baseline_implementation.tcl
viv eto "$W/ax7101-ExtraTimingOpt" baseline_implementation.tcl
stamp CHAIN-COMPLETE
