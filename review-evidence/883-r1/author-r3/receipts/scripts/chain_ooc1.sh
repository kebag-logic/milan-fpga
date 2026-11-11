#!/usr/bin/env bash
# chain_ooc1.sh: ooc-1x1 from route-1x1's finished synthesis log (pp_baseline.py reads only the wrapper's parameter
# block from it), --single-thread-synthesis and --integrated-clock, through the slot wrapper. Writes $L/chain_ooc1.rc.
set -u
here=$(cd "$(dirname "$0")" && pwd)
V=<scratch>/viv; R1=$V/gclone; L=$V/logs; W=$V/w
M=<mgmt>/2026-09-23
stamp() { echo "== $1 $(date -u +%FT%TZ)"; }
rm -f "$L/chain_ooc1.rc"
grep -q "write_checkpoint -force alinx_ax7101_synth.dcp" "$W/ax7101/gateware/baseline.log" \
  || { echo "no synthesis checkpoint yet"; echo 1 > "$L/chain_ooc1.rc"; exit 1; }
source "$here/env.sh"
export PATH="<litex>/venv/bin:$PATH"
( cd "$R1" && python3 syn/ooc/pp_baseline.py "$W/ax7101/gateware" --single-thread-synthesis --output "$W/ax7101-ooc" \
    --integrated-log "$W/ax7101/gateware/baseline.log" --integrated-clock ) > "$L/ooc-prep.log" 2>&1 \
  || { echo "OOC-PREP FAILED"; echo 1 > "$L/chain_ooc1.rc"; exit 1; }
stamp "SLOT-WAIT ooc1"
bash "$M/vivado-slot.sh" systemd-run --user --scope --quiet --unit="milan-883-a768-viv-ooc1-$$" -p MemoryMax=14G \
  bash "$here/viv.sh" "$W/ax7101-ooc" baseline_ooc.tcl > "$L/ooc1.slot.log" 2>&1
rc=$?
stamp "DONE ooc1 rc=$rc"
echo "$rc" > "$L/chain_ooc1.rc"
