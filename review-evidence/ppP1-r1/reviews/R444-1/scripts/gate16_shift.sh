#!/usr/bin/env bash
# R444-1: move only T30's feed start in phase_crf of the parent's
# tb/verilator/milan_dp_render/sim_tdm8_render.cpp (line 3060 at dev bbf704ec)
# by CYCLES. Usage: gate16_shift.sh PARENT_COPY CYCLES
F="$1/tb/verilator/milan_dp_render/sim_tdm8_render.cpp"
sed -n 3053p "$F" | grep -q "void TdmRenderHarness::phase_crf()" || { echo "phase_crf not at 3053"; exit 2; }
sed -i "3060s/next_pdu_at = axis_cycle + 64;/next_pdu_at = axis_cycle + 64 + $2;  \/\/ R444 PROBE/" "$F"
sed -n 3060p "$F"
