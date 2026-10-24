#!/usr/bin/env bash
# route_vivado.sh <repo> <work>: the route-1x1 Vivado run of an exported
# shipping 1x1 build (route_export.sh), then the resource gate against the
# committed record. Started alone as
#   setsid nohup flock $VIVADO_LOCK route_vivado.sh <repo> <work> > <log> 2>&1 &
# so the exclusive lock covers the whole run. Waits for MemAvailable > 20 GB.
# The export's three links (builder out, the two ROM images) are restored for
# the run, since the netlist names them, and removed after it.
set -uo pipefail
REPO=$1; WORK=$2
export PATH="<home>/Xilinx/2026.1/Vivado/bin:$PATH"
stamp() { echo "== $1 $(date -u +%FT%TZ) MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB"; }
stamp LOCKED
mem=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
while [ "$mem" -lt 20971520 ]; do echo "waiting: MemAvailable $mem kB"; sleep 60; mem=$(awk '/MemAvailable/{print $2}' /proc/meminfo); done
cd "$REPO" || exit 2
git rev-parse HEAD; git status --porcelain
test ! -e sw/builder/out && test ! -e configs/generated/ltn_rom.hex && test ! -e configs/generated/ucode.hex || exit 2
ln -s "$WORK/builder" sw/builder/out
ln -s "$WORK/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
ln -s "$WORK/roms/ucode.hex" configs/generated/ucode.hex
cleanup() {
  cd "$REPO"
  [ -L sw/builder/out ] && unlink sw/builder/out
  [ -L configs/generated/ltn_rom.hex ] && unlink configs/generated/ltn_rom.hex
  [ -L configs/generated/ucode.hex ] && unlink configs/generated/ucode.hex
  true
}
trap cleanup EXIT
stamp VIVADO-START
vrc=0
( cd "$WORK/ax7101/gateware" && vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log > vivado.out 2>&1 ) || vrc=$?
stamp "VIVADO-END rc=$vrc"
cleanup
git status --porcelain
grc=0
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1 > "$WORK/route-1x1-check.log" 2>&1 || grc=$?
echo "GATE route-1x1 rc=$grc"
cat "$WORK/route-1x1-check.log"
stamp ROUTE-DONE
