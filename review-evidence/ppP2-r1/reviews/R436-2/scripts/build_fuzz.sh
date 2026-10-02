#!/bin/sh
# Build pause_fuzz.cpp against one copy of KL_pp_nvm_port.sv at one deadline.
#   build_fuzz.sh <path/to/KL_pp_nvm_port.sv> <MEM_TIMEOUT_CYC_P> <out dir>
# VERILATOR must name the pinned 5.050 wrapper.
set -eu
RTL=$1; T=$2; OUT=$3
HERE=$(cd "$(dirname "$0")" && pwd)
: "${VERILATOR:?set VERILATOR to the pinned wrapper}"
mkdir -p "$OUT"
"$VERILATOR" --cc --exe --build -j 2 --top-module KL_pp_nvm_port \
  -Wno-fatal -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDSIGNAL \
  -GMAX_PAYLOAD_P=1024 -GMEM_TIMEOUT_CYC_P="$T" \
  -CFLAGS "-std=c++17 -O2 -DTMO=$T" \
  --Mdir "$OUT" "$RTL" "$HERE/pause_fuzz.cpp" -o Vfuzz > "$OUT/build.log" 2>&1
