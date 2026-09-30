#!/bin/sh
# Build and run tb/pp_top's second (SRP_VID fixture) build exactly as the
# Makefile's `run` target does, but with Verilator's build capped at 8 jobs.
# Usage: pp_top_vid_leg.sh <tree-root>   (verilator must be on PATH)
set -eu
cd "$1/tb/pp_top"
H=../../hdl
SRCS="$H/common/pp_pkg.sv $H/srp/srp_pkg.sv $H/acmp/pp_acmp_pkg.sv $H/adp/pp_adp_pkg.sv \
$H/common/KL_pp_prng.sv $H/common/KL_pp_timer_service.sv \
$H/packet_engine/KL_pp_rx_validator.sv $H/packet_engine/KL_pp_rx_slots.sv \
$H/packet_engine/KL_pp_normalizer.sv $H/packet_engine/KL_pp_dispatch.sv \
$H/packet_engine/KL_pp_tx_slots.sv $H/packet_engine/KL_pp_release_merge.sv \
$H/packet_engine/KL_pp_tx_arbiter.sv $H/packet_engine/KL_pp_scoreboard.sv \
$H/packet_engine/KL_pp_event_router.sv $H/packet_engine/KL_pp_originator.sv \
$H/packet_engine/KL_pp_trace_ring.sv $H/packet_engine/KL_pp_side_port.sv \
$H/packet_engine/KL_pp_nvm_port.sv $H/packet_engine/KL_pp_nvm_mgr_arb.sv \
$H/aecp/ucpu_pkg.sv $H/aecp/KL_aecp_ucpu.sv $H/aecp/KL_aecp_desc_mem_guard.sv \
$H/aecp/KL_aecp_desc_store.sv $H/aecp/KL_aecp_dyn_state.sv $H/aecp/KL_aecp_engine.sv \
$H/aecp/KL_aecp_resp_buf.sv $H/aecp/KL_aecp_nvm_writer.sv \
$H/aecp/KL_aecp_notify.sv $H/aecp/KL_aecp_ca_originator.sv $H/adp/KL_adp_engine.sv \
$H/acmp/KL_pp_acmp_listener.sv $H/acmp/KL_acmp_talker.sv $H/acmp/KL_pp_acmp_lsn_admit.sv \
$H/acmp/KL_acmp_nvm_shadow.sv $H/maap/KL_pp_maap.sv \
$H/srp/KL_srp_decoder.sv $H/srp/KL_srp_domain.sv $H/srp/KL_srp_vlan.sv \
$H/srp/KL_srp_admission.sv $H/srp/KL_srp_talker_fsm.sv $H/srp/KL_srp_listener_fsm.sv \
$H/srp/KL_srp_encoder.sv $H/srp/KL_srp_top.sv \
$H/top/KL_mrp_strip.sv $H/top/protocol_processor_top.sv pp_top_wrap.sv"
# shellcheck disable=SC2086
verilator --cc --exe --build -j 8 --top-module pp_top_wrap \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
  -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -CFLAGS "-std=c++17 -O2 -I$(pwd) -Wall -Wextra" \
  "+define+PP_TOP_SRP_DOM_DEF_VID=16'h5A3C" \
  -CFLAGS "-DPP_TOP_SRP_DOM_DEF_VID=0x5A3C -Wall -Wextra" \
  --Mdir obj_vid $SRCS sim_main.cpp -o Vpp_top_vid
./obj_vid/Vpp_top_vid
