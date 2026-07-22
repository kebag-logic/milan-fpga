#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Open-toolchain synthesis check: prove the (XPM-free) RTL maps to a *generic*,
# device-independent cell library with Yosys — i.e. it will build on non-Xilinx
# FPGAs. SystemVerilog (interfaces, packages, assignment patterns) is converted to
# Verilog-2005 by sv2v first. `hierarchy -check` fails if any vendor/undefined
# primitive remains, so a PASS means the module is fully mapped to generic logic.
#
#   ./run.sh                 # generic synth of every top below
#   YOSYS_SYNTH=synth_ecp5 ./run.sh   # target a real device (Lattice ECP5)
#
# Requires: yosys, and sv2v on PATH (see README.md).

set -u
export PATH="$HOME/.local/bin:$PATH"
R="$(cd "$(dirname "$0")/../.." && pwd)"
A="$R/third_party/verilog-axis/rtl"
C="$R/hdl/common"; Q="$R/hdl/ieee8021q/ts"; P="$R/hdl/ieee8021as/ptp_timestamp"
E="$R/hdl/common/eth_event_counter"; D="$R/hdl/ieee17221/adp"; K="$R/hdl/ieee17221/aecp"; M="$R/hdl/ieee17221/acmp"
S="$R/hdl/ieee8021q/srp"; F="$R/hdl/ieee8021q/filtering"
INC="-DSYNTHESIS -I $R/hdl/common -I $Q -I $E -I $D -I $P -I $K -I $K/gen"
SYNTH="${YOSYS_SYNTH:-synth}"           # generic 'synth' = device-independent
TMP="$(mktemp -d)"

AECP_SRCS="$K/aecp_pkg.sv $K/KL_aecp_ingress.sv $K/KL_aecp_packet_validator.sv $K/KL_aecp_common_parser.sv $K/KL_aecp_l0_state.sv $K/KL_aecp_timers.sv $K/KL_aecp_accessor.sv $K/KL_aecp_aem_store.sv $K/KL_aecp_aem_dyn_mux.sv $K/KL_aecp_response_builder.sv $K/KL_aecp_top.sv"
LWSRP_SRCS="$S/lwsrp_pkg.sv $S/KL_lwsrp_timers.sv $S/KL_lwsrp_tx.sv $S/KL_lwsrp_ingress.sv $S/KL_lwsrp_walker.sv $S/KL_lwsrp_registrar.sv $S/KL_lwsrp_ta_registrar.sv $S/KL_lwsrp_rx.sv $S/KL_lwsrp_bw_gate.sv $S/KL_lwsrp_ctx.sv $S/KL_lwsrp_ctx_tx.sv $S/KL_lwsrp_top.sv"

for t in sv2v yosys; do command -v $t >/dev/null || { echo "missing tool: $t (see syn/yosys/README.md)"; exit 2; }; done

# top | source files (interface modules go through their flat wrapper)
tops=(
  "tcam|$F/tcam.sv"
  "cdc_pulse|$C/cdc_pulse.sv"
  "cdc_handshake|$C/cdc_handshake.sv"
  "adp_tx_arbiter|$D/adp_tx_arbiter.sv"
  "adp_advertiser|$D/adp_pkg.sv $D/adp_advertiser.sv"
  "rx_mac_filter|$F/tcam.sv $F/rx_mac_filter.sv $C/tx_ifg_gasket.sv"
  "milan_csr|$R/hdl/common/csr/milan_csr.sv"
  "KL_acmp_tlkr_ctx|$M/acmp_pkg.sv $M/KL_acmp_tlkr_ctx.sv"
  "KL_acmp_lstn_ctx|$M/acmp_pkg.sv $M/KL_acmp_lstn_ctx.sv"
  "KL_acmp_responder|$M/acmp_pkg.sv $M/KL_acmp_tlkr_ctx.sv $M/KL_acmp_responder.sv"
  "KL_acmp_listener|$M/acmp_pkg.sv $M/KL_acmp_lstn_ctx.sv $M/KL_acmp_listener.sv"
  "KL_avtp_rx_monitor|$R/hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv"
  "KL_stream_table|$R/hdl/ieee1722/avtp/KL_stream_table.sv"
  "KL_avtp_rx_monitor_ctx|$R/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
  "KL_pcm_route|$R/hdl/ieee1722/aaf/KL_pcm_route.sv"
  "KL_aaf_capture_i2s|$C/cdc_pair_fifo.sv $R/hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv"
  "KL_aaf_packetizer|$R/hdl/ieee1722/aaf/KL_aaf_packetizer.sv"
  "KL_crf_rx|$R/hdl/ieee1722/crf/KL_crf_rx.sv"
  "KL_crf_tx|$C/cdc_pulse.sv $R/hdl/ieee1722/crf/KL_crf_tx.sv"
  "KL_link_guard|$C/KL_link_guard.sv"
  "KL_maap|$R/hdl/ieee1722/maap/KL_maap.sv"
  "KL_i2s_playback|$C/cdc_pair_fifo.sv $C/cdc_pulse.sv $R/hdl/ieee1722/aaf/KL_i2s_playback.sv"
  "KL_tone_gen|$R/hdl/ieee1722/aaf/KL_tone_gen.sv"
  "KL_aaf_rx_depacketizer|$A/axis_fifo.v $R/hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv"
  "KL_lwsrp_top|$A/axis_fifo.v $LWSRP_SRCS"
  "KL_aecp_top|$C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $D/adp_pkg.sv $A/axis_fifo.v $AECP_SRCS"
  "credit_based_shaper|$C/ethernet_packet_pkg.sv $Q/credit_based_shaper.sv"
  "timestamp_counter|$P/timestamp_counter.sv"
  "ptp_csr_sync|$P/ptp_csr_sync.sv"
  "event_counter|$E/event_counter.sv"
  "ethernet_events|$E/ethernet_events.sv $E/event_counter.sv"
  "classifier_wrap|$C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $Q/traffic_class_map.sv $Q/traffic_classifier.sv $A/axis_fifo.v $R/tb/verilator/classifier/classifier_wrap.sv"
  "queues_wrap|$C/axi_stream_if.sv $Q/traffic_queues.sv $A/axis_fifo.v $A/axis_demux.v $A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v $R/tb/verilator/queues/queues_wrap.sv"
  "axis_fifo|$A/axis_fifo.v"
  "axis_demux|$A/axis_demux.v"
  "axis_arb_mux|$A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v"
  "milan_datapath|$C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $D/adp_pkg.sv $A/axis_fifo.v $A/axis_demux.v $A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v $Q/traffic_class_map.sv $Q/traffic_classifier.sv $Q/credit_based_shaper.sv $Q/traffic_shaping_core.sv $Q/traffic_queues.sv $Q/traffic_controller_802_1q.sv $P/timestamp_counter.sv $P/ptp_csr_sync.sv $C/cdc_pulse.sv $C/cdc_handshake.sv $C/axis_mux_rr_2in_1out.sv $P/ptp_ts_core.sv $P/ptp_ts_top.sv $F/tcam.sv $F/rx_mac_filter.sv $C/tx_ifg_gasket.sv $R/hdl/ieee1722/aaf/KL_pcm_lpf.sv $C/KL_link_guard.sv $AECP_SRCS $M/acmp_pkg.sv $M/KL_acmp_tlkr_ctx.sv $M/KL_acmp_responder.sv $M/KL_acmp_lstn_ctx.sv $M/KL_acmp_listener.sv $LWSRP_SRCS $D/adp_advertiser.sv $D/adp_tx_arbiter.sv $E/ethernet_events.sv $E/event_counter.sv $R/hdl/common/csr/milan_csr.sv $R/hdl/ieee1722/aaf/aaf_talker_i2s.sv $R/hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv $R/hdl/ieee1722/avtp/avtp_subtype_pkg.sv $R/hdl/ieee1722/avtp/avtp_stream_parser.sv $R/hdl/ieee1722/avtp/KL_stream_table.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv $R/hdl/ieee1722/crf/KL_crf_rx.sv $R/hdl/ieee1722/crf/KL_crf_tx.sv $R/hdl/ieee1722/maap/KL_maap.sv $R/hdl/ieee1722/aaf/KL_i2s_playback.sv $R/hdl/ieee1722/aaf/KL_tone_gen.sv $R/hdl/ieee1722/aaf/KL_media_adv.sv $C/cdc_pair_fifo.sv $R/hdl/ieee1722/aaf/KL_pcm_route.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv $R/hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv $R/hdl/ieee1722/aaf/KL_aaf_packetizer.sv $R/hdl/milan/milan_datapath.sv"
)

echo "== Yosys open-synthesis check ($SYNTH, via sv2v) =="
pass=0; fail=0
for spec in "${tops[@]}"; do
  top="${spec%%|*}"; srcs="${spec#*|}"
  if ! sv2v --top="$top" $INC $srcs > "$TMP/$top.v" 2> "$TMP/$top.sv2v.err"; then
    printf "  [FAIL] %-22s sv2v: %s\n" "$top" "$(head -1 "$TMP/$top.sv2v.err")"; fail=$((fail+1)); continue
  fi
  yosys -p "read_verilog $TMP/$top.v; $SYNTH -top $top; hierarchy -check; stat" > "$TMP/$top.yos.log" 2>&1
  rc=$?
  cells="$(grep -E '^[[:space:]]+[0-9]+ cells$' "$TMP/$top.yos.log" | head -1 | grep -oE '[0-9]+')"
  if [ $rc -eq 0 ]; then printf "  [PASS] %-22s cells=%s\n" "$top" "${cells:-?}"; pass=$((pass+1))
  else printf "  [FAIL] %-22s yosys: %s\n" "$top" "$(grep -iE '^ERROR' "$TMP/$top.yos.log" | head -1)"; fail=$((fail+1)); fi
done
echo "--------------------------------------------------------------"
echo "tops: $((pass+fail))   pass: $pass   fail: $fail"
echo "RESULT: $([ $fail -eq 0 ] && echo PASS || echo FAIL)"
rm -rf "$TMP"
# Non-fatal structural report (the RMON tied-bus class): inventory of
# milan_datapath inputs the SoC instantiation ties to constants, so a green
# port-level TB can never again silently vouch for a cone silicon never
# drives. Informational only — never changes this script's RESULT.
"$R/scripts/check_tied_inputs.sh" || true
[ $fail -eq 0 ]
