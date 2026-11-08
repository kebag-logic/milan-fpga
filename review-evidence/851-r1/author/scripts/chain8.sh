#!/usr/bin/env bash
# chain8.sh: ooc-8x8 in the gate clone, out of context only: the 8x8 export, its RTL elaboration for the wrapper's
# parameter block, then the standalone synthesis, each Vivado run through the slot wrapper in its own scope (MemoryMax 14G).
# --single-thread-synthesis and --integrated-clock, as the record was measured. 8x8 is not routed.
set -u
here=$(cd "$(dirname "$0")" && pwd)
S=$VALIDATION_STORAGE/scratch/851-a744; R=$S/gclone8; L=$S/glogs; W8=$S/w8b
# its own clone: the 1x1 chain re-points the shared clone's sw/builder/out link while this one runs
export REPO_OVERRIDE=$R
M=$HOME/milan-fpga-management/2026-09-23
stamp() { echo "== $1 $(date -u +%FT%TZ)"; }
viv() { # name dir script
  stamp "SLOT-WAIT $1"
  bash "$M/vivado-slot.sh" systemd-run --user --scope --quiet --unit="milan-851-a744-viv-$1-$$" -p MemoryMax=14G \
    bash "$here/viv.sh" "$2" "$3" > "$L/$1.slot.log" 2>&1
  rc=$?; stamp "DONE $1 rc=$rc"; [ "$rc" = 0 ] || { echo "$1 FAILED rc=$rc"; exit 1; }
}
mkdir -p "$L"
stamp EXPORT-8x8
bash "$here/export_shape.sh" ax8x8 "$W8" > "$L/export-8x8.log" 2>&1 || { echo "EXPORT FAILED rc=$?"; exit 1; }
source "$here/env.sh"
export PATH="$HOME/litex-milan/venv/bin:$PATH"
G=$W8/ax8x8/gateware; X=$W8/ax8x8-rtl
( cd "$R" && python3 syn/ooc/pp_baseline.py "$G" --synthesis-only --single-thread-synthesis ) > "$L/prep-8x8.log" 2>&1 || { echo PREP FAILED; exit 1; }
mkdir -p "$X"; cp "$G"/*.xdc "$X"/; cp "$G"/*.init "$X"/ 2>/dev/null
python3 -B "$here/cut_rtl.py" "$G/baseline_integrated.tcl" "$X/rtl.tcl" || { echo CUT FAILED; exit 1; }
viv rtl8 "$X" rtl.tcl
stamp OOC-PREP
( cd "$R" && python3 syn/ooc/pp_baseline.py "$G" --single-thread-synthesis --output "$W8/ax8x8-ooc" \
    --integrated-log "$X/baseline.log" --integrated-clock ) > "$L/ooc-prep-8x8.log" 2>&1 || { echo OOC-PREP FAILED; exit 1; }
viv ooc8 "$W8/ax8x8-ooc" baseline_ooc.tcl
stamp CHAIN-COMPLETE
