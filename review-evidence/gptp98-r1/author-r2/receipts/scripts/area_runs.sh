#!/bin/bash
# Placed OOC engine runs: base and head RTL, each with the same shipping
# image (the image is unchanged: hdl/ucode is identical at base and head).
set -euo pipefail
S=<scratch>; R=$S/runs; A=$S/area
. "$HOME/Xilinx/2026.1/Vivado/settings64.sh"
run() { # tag repo image
  mkdir -p "$A/$1"; cp "$3" "$A/$1/gptp_ucode.hex"
  (cd "$A/$1" && vivado -mode batch -nojournal -log "$1.log" -source "$S/scripts/engine_place.tcl" -tclargs "$2" "$1" > "$1.console" 2>&1)
  echo "$1 done rc=$?"
}
run base "$R/base-fast" "$R/base-fast/syn/ooc/work/gptp_ucode.hex"
run head "$R/head2-fast" "$R/head2-fast/syn/ooc/work/gptp_ucode.hex"
echo all done
