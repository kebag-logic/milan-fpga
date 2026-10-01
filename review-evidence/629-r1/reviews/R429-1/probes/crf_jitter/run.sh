#!/bin/sh
# Disposable review probe (R429-1). Usage: run.sh <milan-fpga checkout> <verilator> <workdir>
# Builds tb_crf_jitter.sv against the checkout's KL_crf_rx.sv and prints the PROBE lines.
set -eu
SRC="$1"; VL="$2"; W="$3"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$W"
"$VL" --version
"$VL" --binary --timing -Wno-fatal -Wno-WIDTH -Wno-UNUSEDSIGNAL --top-module tb_crf_jitter \
  -Mdir "$W/obj" "$SRC/hdl/ieee1722/crf/KL_crf_rx.sv" "$HERE/tb_crf_jitter.sv" > "$W/build.log" 2>&1
"$W/obj/Vtb_crf_jitter"
