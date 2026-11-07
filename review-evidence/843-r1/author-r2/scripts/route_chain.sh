#!/usr/bin/env bash
# route_chain.sh <rev> <tag>: route-1x1's set at <rev>, one Vivado run at a time through the slot wrapper:
# the shipping directive (ExtraPostPlacementOpt), then AltSpreadLogic_high and ExtraTimingOpt from its synthesis
# checkpoint. Each Vivado run sits in its own scope (MemoryMax 14G) and inherits this unit's CPUs. Then the gate's
# check on the set against the record. Stops at the first failed step.
set -u
rev=$1; tag=$2; here=$(cd "$(dirname "$0")" && pwd)
S=$VALIDATION_STORAGE/scratch/843-a737b/route-$tag; W=$S/w; R=$S/clone; L=$S/logs
M=$HOME/milan-fpga-management/2026-09-23
stamp() { echo "== $1 $(date -u +%FT%TZ) MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB"; }
viv() { # name dir script
  stamp "SLOT-WAIT $1"
  bash "$M/vivado-slot.sh" systemd-run --user --scope --quiet --unit="milan-843-a737b-viv-$tag-$1-$$" -p MemoryMax=14G \
    bash "$here/viv.sh" "$2" "$3" > "$L/$1.slot.log" 2>&1
  rc=$?; stamp "DONE $1 rc=$rc"; [ "$rc" = 0 ] || { echo "$1 FAILED rc=$rc"; exit 1; }
}
mkdir -p "$L"
stamp "EXPORT $rev"
bash "$here/route_export.sh" "$rev" "$tag" > "$L/export.log" 2>&1 || { echo "EXPORT FAILED rc=$?"; tail -20 "$L/export.log"; exit 1; }
viv eppo "$W/ax7101/gateware" baseline_integrated.tcl
source "$here/env.sh"
export PATH="$HOME/litex-milan/venv/bin:$PATH"
python3 -B "$here/dir_prep.py" "$R" "$W" > "$L/dir-prep.log" 2>&1 || { echo DIR-PREP FAILED; exit 1; }
viv aslh "$W/ax7101-AltSpreadLogic_high" baseline_implementation.tcl
viv eto "$W/ax7101-ExtraTimingOpt" baseline_implementation.tcl
stamp GATE
( cd "$R" && python3 syn/ooc/pp_resource_gate.py check "$W/ax7101/gateware" --endpoint route-1x1 \
    --comparison "$W/ax7101-AltSpreadLogic_high" --comparison "$W/ax7101-ExtraTimingOpt" ) > "$L/gate-check.log" 2>&1
echo "gate check rc=$?" | tee "$L/gate-check.rc"
stamp CHAIN-COMPLETE
