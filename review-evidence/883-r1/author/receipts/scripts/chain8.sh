#!/usr/bin/env bash
# chain8.sh: ooc-8x8 (the 8x8 export, its RTL elaboration for the wrapper's parameter block, the standalone synthesis)
# in its own clone, then ooc-1x1 once route-1x1's synthesis log exists. --single-thread-synthesis and --integrated-clock,
# as the record was measured. One Vivado run at a time through the slot wrapper. Writes $L/chain8.rc at the end.
set -u
here=$(cd "$(dirname "$0")" && pwd)
V=<scratch>/viv; R=$V/gclone8; R1=$V/gclone; L=$V/logs; W8=$V/w8; W=$V/w
M=<mgmt>/2026-09-23
stamp() { echo "== $1 $(date -u +%FT%TZ)"; }
fail() { echo "$1"; echo 1 > "$L/chain8.rc"; exit 1; }
viv() { # name dir script
  stamp "SLOT-WAIT $1"
  bash "$M/vivado-slot.sh" systemd-run --user --scope --quiet --unit="milan-883-a768-viv-$1-$$" -p MemoryMax=14G \
    bash "$here/viv.sh" "$2" "$3" > "$L/$1.slot.log" 2>&1
  rc=$?; stamp "DONE $1 rc=$rc"; [ "$rc" = 0 ] || fail "$1 FAILED rc=$rc"
}
mkdir -p "$L"; rm -f "$L/chain8.rc"
stamp EXPORT-8x8
bash "$here/export_shape.sh" ax8x8 "$W8" "$R" > "$L/export-8x8.log" 2>&1 || fail "EXPORT FAILED rc=$?"
source "$here/env.sh"
export PATH="<litex>/venv/bin:$PATH"
G=$W8/ax8x8/gateware; X=$W8/ax8x8-rtl
( cd "$R" && python3 syn/ooc/pp_baseline.py "$G" --synthesis-only --single-thread-synthesis ) > "$L/prep-8x8.log" 2>&1 || fail "PREP FAILED"
mkdir -p "$X"; cp "$G"/*.xdc "$X"/; cp "$G"/*.init "$X"/ 2>/dev/null
python3 -B "$here/cut_rtl.py" "$G/baseline_integrated.tcl" "$X/rtl.tcl" || fail "CUT FAILED"
viv rtl8 "$X" rtl.tcl
( cd "$R" && python3 syn/ooc/pp_baseline.py "$G" --single-thread-synthesis --output "$W8/ax8x8-ooc" \
    --integrated-log "$X/baseline.log" --integrated-clock ) > "$L/ooc-prep-8x8.log" 2>&1 || fail "OOC-PREP-8 FAILED"
viv ooc8 "$W8/ax8x8-ooc" baseline_ooc.tcl
stamp WAIT-EPPO-SYNTH
while ! { [ -f "$W/ax7101/gateware/baseline.log.rc" ] || [ -f "$L/chain1.rc" ]; }; do sleep 60; done
[ "$(cut -d' ' -f1 "$W/ax7101/gateware/baseline.log.rc" 2>/dev/null)" = 0 ] || fail "EPPO not rc 0; no ooc-1x1"
( cd "$R1" && python3 syn/ooc/pp_baseline.py "$W/ax7101/gateware" --single-thread-synthesis --output "$W/ax7101-ooc" \
    --integrated-log "$W/ax7101/gateware/baseline.log" --integrated-clock ) > "$L/ooc-prep.log" 2>&1 || fail "OOC-PREP FAILED"
viv ooc1 "$W/ax7101-ooc" baseline_ooc.tcl
stamp CHAIN-COMPLETE
echo 0 > "$L/chain8.rc"
