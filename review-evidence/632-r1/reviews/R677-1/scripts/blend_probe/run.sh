#!/usr/bin/env bash
# Review probe: the Arty blend shape's two capture interfaces on one domain.
# Usage: run.sh <checkout of f1fda3f1> <work dir>; $VERILATOR is a 5.050.
set -euo pipefail
H=$(cd "$1" && pwd)/hdl
W=$(mkdir -p "$2" && cd "$2" && pwd)
here=$(cd "$(dirname "$0")" && pwd)
"${VERILATOR:-verilator}" --cc --exe --build -j 4 -Wno-fatal -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
  --Mdir "$W/obj" --top-module blend_wrap \
  "$H/ieee1722/crf/KL_media_if_latency_pkg.sv" "$H/common/cdc_pair_fifo.sv" \
  "$H/ieee1722/aaf/KL_aaf_capture_i2s.sv" "$H/ieee1722/aaf/KL_tdm_capture_master.sv" \
  "$H/ieee1722/aaf/KL_pair_blend.sv" "$H/ieee1722/crf/KL_media_domain_event.sv" \
  "$here/blend_wrap.sv" "$here/sim_blend.cpp" -o Vblend
"$W/obj/Vblend"
