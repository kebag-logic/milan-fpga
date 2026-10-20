#!/usr/bin/env bash
# ooc-1x1 per docs/testing/PP_SHADOW_BASELINE_RECIPE.md (standalone, --integrated-clock), from a route's export.
# usage: ooc1x1.sh <route-label> <repo>
set -uo pipefail
label=$1; export REPO=$2
W=<scratch>/route-$label/work
export PATH="<home>/Xilinx/2026.1/Vivado/bin:$PATH"
export TMPDIR=<scratch>/tmp
cd "$REPO" || exit 2
date -u +%FT%TZ; git rev-parse HEAD
test ! -e sw/builder/out && ln -s "$W/builder" sw/builder/out
test ! -e configs/generated/ltn_rom.hex && ln -s "$W/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
test ! -e configs/generated/ucode.hex && ln -s "$W/roms/ucode.hex" configs/generated/ucode.hex
cleanup() {
  cd "$REPO"
  [ -L sw/builder/out ] && unlink sw/builder/out
  [ -L configs/generated/ltn_rom.hex ] && unlink configs/generated/ltn_rom.hex
  [ -L configs/generated/ucode.hex ] && unlink configs/generated/ucode.hex
  true
}
trap cleanup EXIT
rc=0
python3 syn/ooc/pp_baseline.py "$W/ax7101/gateware" --single-thread-synthesis \
  --output "$W/ax7101-ooc" --integrated-log "$W/ax7101/gateware/baseline.log" --integrated-clock || rc=$?
echo "EXPORT rc=$rc"
[ "$rc" -eq 0 ] || exit 1
vrc=0
( cd "$W/ax7101-ooc" && flock -x $VIVADO_LOCK vivado -mode batch -source baseline_ooc.tcl -nojournal -log baseline.log > vivado.out 2>&1 ) || vrc=$?
echo "VIVADO rc=$vrc"; date -u +%FT%TZ
grc=0
python3 syn/ooc/pp_resource_gate.py check "$W/ax7101-ooc" --endpoint ooc-1x1 || grc=$?
echo "GATE rc=$grc"; date -u +%FT%TZ
