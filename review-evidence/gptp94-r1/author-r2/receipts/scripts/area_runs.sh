#!/bin/bash
# Four placed OOC engine runs: base and head, each with its own default
# image, then each RTL with the other's image (the attribution pair).
set -euo pipefail
S=<scratch>; R=$S/runs; A=$S/area
. "$HOME/Xilinx/2026.1/Vivado/settings64.sh"
run() { # tag repo image
  mkdir -p "$A/$1"; cp "$3" "$A/$1/gptp_ucode.hex"
  (cd "$A/$1" && vivado -mode batch -nojournal -log "$1.log" -source "$S/scripts/engine_place.tcl" -tclargs "$2" "$1" > "$1.console" 2>&1)
  echo "$1 done rc=$?"
}
run base-rtl-base-img "$R/base-fast" "$R/base-fast/syn/ooc/work/gptp_ucode.hex"
run head-rtl-head-img "$R/head-fast" "$R/head-fast/syn/ooc/work/gptp_ucode.hex"
run head-rtl-base-img "$R/head-fast" "$R/base-fast/syn/ooc/work/gptp_ucode.hex"
run base-rtl-head-img "$R/base-fast" "$R/head-fast/syn/ooc/work/gptp_ucode.hex"
echo all done
