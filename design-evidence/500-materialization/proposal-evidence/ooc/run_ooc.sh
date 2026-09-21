#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Every area figure of the design page, one ooc_measure.sh row each, written
# to results_ooc.txt beside this file. Run from anywhere inside the evidence
# checkout; the processor sources are the pinned submodule's.
#
#   run_ooc.sh            # all rows (a few minutes, one yosys at a time)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$here/../../../.." && pwd)"
pe="$here/.."
pp="$root/protocol-processor/hdl"
m="$here/ooc_measure.sh"
out="$here/results_ooc.txt"
S11="N_STREAM_IN_P=2 N_STREAM_OUT_P=2 N_SPORT_IN_P=1 N_SPORT_OUT_P=1 N_AUDIO_UNIT_P=1 N_CLK_DOM_P=1"
S88="N_STREAM_IN_P=9 N_STREAM_OUT_P=9 N_SPORT_IN_P=8 N_SPORT_OUT_P=8 N_AUDIO_UNIT_P=1 N_CLK_DOM_P=1"
W11="$S11 N_NAME_P=38 MAPI_CLS_P=8'd8 MAPO_CLS_P=8'd17 MAP_ENT_MAX_P=17"
W88="$S88 N_NAME_P=99 MAPI_CLS_P=64'd0 MAPO_CLS_P=64'd651061555542690057 MAP_ENT_MAX_P=9"
rows=(
  # label | top | params | nodsp | sources
  "cal-backend-1x1-n30|KL_nvm_backend|$S11 N_NAME_P=30|0|$root/hdl/milan/KL_nvm_backend.sv"
  "cal-backend-1x1-n38|KL_nvm_backend|$S11 N_NAME_P=38|0|$root/hdl/milan/KL_nvm_backend.sv"
  "cal-backend-8x8-n99|KL_nvm_backend|$S88 N_NAME_P=99|0|$root/hdl/milan/KL_nvm_backend.sv"
  "cal-port|KL_pp_nvm_port||0|$pp/packet_engine/KL_pp_nvm_port.sv"
  "cal-bindmgr-1x1|KL_acmp_nvm_shadow|N_SINKS_P=2|0|$pp/acmp/pp_acmp_pkg.sv $pp/acmp/KL_acmp_nvm_shadow.sv"
  "cal-bindmgr-8x8|KL_acmp_nvm_shadow|N_SINKS_P=9|0|$pp/acmp/pp_acmp_pkg.sv $pp/acmp/KL_acmp_nvm_shadow.sv"
  "b-writer-1x1|KL_aecp_nvm_writer|$W11|0|$pe/prototype/KL_aecp_nvm_writer.proto.sv"
  "b-writer-1x1-nodsp|KL_aecp_nvm_writer|$W11|1|$pe/prototype/KL_aecp_nvm_writer.proto.sv"
  "b-writer-8x8|KL_aecp_nvm_writer|$W88|0|$pe/prototype/KL_aecp_nvm_writer.proto.sv"
  "b-writer-8x8-nodsp|KL_aecp_nvm_writer|$W88|1|$pe/prototype/KL_aecp_nvm_writer.proto.sv"
  "b-arbiter|KL_pp_nvm_mgr_arb||0|$pe/prototype/KL_pp_nvm_mgr_arb.proto.sv"
  "a-manager-unit|KL_acmp_nvm_shadow|N_SINKS_P=1|0|$pp/acmp/pp_acmp_pkg.sv $pp/acmp/KL_acmp_nvm_shadow.sv"
  "a-shadows-1x1|d3a_shadow_proxy|N_STREAM_IN_P=2 N_STREAM_OUT_P=2 N_MAP_ENT_P=25 N_NAME_P=38|0|$here/d3a_shadow_proxy.sv"
  "a-shadows-8x8|d3a_shadow_proxy|N_STREAM_IN_P=9 N_STREAM_OUT_P=9 N_MAP_ENT_P=72 N_NAME_P=99|0|$here/d3a_shadow_proxy.sv"
  "c-fabric-1x1|d3c_fabric_proxy|N_STREAM_IN_P=2 N_STREAM_OUT_P=2 N_SPORT_IN_P=1 N_SPORT_OUT_P=1 N_NAME_P=38|0|$here/d3c_fabric_proxy.sv"
  "c-fabric-8x8|d3c_fabric_proxy|N_STREAM_IN_P=9 N_STREAM_OUT_P=9 N_SPORT_IN_P=8 N_SPORT_OUT_P=8 N_NAME_P=99|0|$here/d3c_fabric_proxy.sv"
)
{
  printf "%-34s %-26s %6s %6s %7s %6s %6s %6s %4s %6s\n" label top LUT LUTRAM LUT_TOT FF RAMB36 RAMB18 DSP CARRY4
  for r in "${rows[@]}"; do
    IFS='|' read -r label top params nodsp srcs <<< "$r"
    # shellcheck disable=SC2086
    "$m" "$label" "$top" "$params" "$nodsp" $srcs
  done
} | tee "$out"
