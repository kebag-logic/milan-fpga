#!/usr/bin/env bash
# usage: run_probe.sh <KL_chan_map_capture.sv> <objdir> ; prints the probe log
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
verilator --binary --timing -j 8 -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
  -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
  --top-module tb_probe --Mdir "$2" "$1" "$here/tb_probe.sv" -o Vtb_probe >/dev/null
"$2/Vtb_probe"
