#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Out-of-context AREA measurement for one (or a few) tops, mapped to the real
# xc7 cell library. run.sh answers "does it map to generic logic"; this answers
# "how many LUTs/FFs/BRAMs does it cost", which is the only number an area
# lever may be judged on.
#
# WHY -flatten: a hierarchical synth's `stat` counts TOP-LEVEL cells only, so a
# lever inside a submodule reads as zero. Flatten first, then stat.
#
#   ./ooc.sh                       # every top in the AREA list below
#   ./ooc.sh KL_chan_map_render    # just these tops
#
# Requires: yosys, sv2v (see README.md).

set -u
export PATH="$HOME/.local/bin:$PATH"
R="$(cd "$(dirname "$0")/../.." && pwd)"
A="$R/third_party/verilog-axis/rtl"
C="$R/hdl/common"; Q="$R/hdl/ieee8021q/ts"; P="$R/hdl/ieee8021as/ptp_timestamp"
E="$R/hdl/common/eth_event_counter"; D="$R/hdl/ieee17221/adp"; K="$R/hdl/ieee17221/aecp"; M="$R/hdl/ieee17221/acmp"
S="$R/hdl/ieee8021q/srp"; F="$R/hdl/ieee8021q/filtering"
INC="-DSYNTHESIS -I $R/hdl/common -I $R/hdl/common/csr -I $Q -I $E -I $D -I $P -I $K -I $K/gen"
TMP="${OOC_TMP:-$(mktemp -d)}"; mkdir -p "$TMP"

AECP_SRCS="$K/aecp_pkg.sv $K/KL_aecp_ingress.sv $K/KL_aecp_packet_validator.sv $K/KL_aecp_common_parser.sv $K/KL_aecp_l0_state.sv $K/KL_aecp_timers.sv $K/KL_aecp_accessor.sv $K/KL_aecp_aem_store.sv $K/KL_aecp_aem_dyn_mux.sv $K/KL_aecp_response_builder.sv $K/KL_aecp_top.sv"
LWSRP_SRCS="$S/lwsrp_pkg.sv $S/KL_lwsrp_timers.sv $S/KL_lwsrp_tx.sv $S/KL_lwsrp_ingress.sv $S/KL_lwsrp_walker.sv $S/KL_lwsrp_registrar.sv $S/KL_lwsrp_ta_registrar.sv $S/KL_lwsrp_rx.sv $S/KL_lwsrp_bw_gate.sv $S/KL_lwsrp_ctx.sv $S/KL_lwsrp_ctx_tx.sv $S/KL_lwsrp_top.sv"
DP_SRCS="$C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $D/adp_pkg.sv $A/axis_fifo.v $A/axis_demux.v $A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v $Q/traffic_class_map.sv $Q/traffic_classifier.sv $Q/credit_based_shaper.sv $Q/traffic_shaping_core.sv $Q/traffic_queues.sv $Q/traffic_controller_802_1q.sv $P/timestamp_counter.sv $P/ptp_csr_sync.sv $C/cdc_pulse.sv $C/cdc_handshake.sv $C/axis_mux_rr_2in_1out.sv $P/ptp_ts_core.sv $P/ptp_ts_top.sv $F/tcam.sv $F/rx_mac_filter.sv $C/tx_ifg_gasket.sv $R/hdl/ieee1722/aaf/KL_pcm_lpf.sv $C/KL_link_guard.sv $AECP_SRCS $M/acmp_pkg.sv $M/KL_acmp_tlkr_ctx.sv $M/KL_acmp_responder.sv $M/KL_acmp_lstn_ctx.sv $M/KL_acmp_listener.sv $LWSRP_SRCS $D/adp_advertiser.sv $D/adp_tx_arbiter.sv $E/ethernet_events.sv $E/event_counter.sv $R/hdl/common/csr/milan_csr.sv $R/hdl/ieee1722/aaf/aaf_talker_i2s.sv $R/hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv $R/hdl/ieee1722/avtp/avtp_subtype_pkg.sv $R/hdl/ieee1722/avtp/avtp_stream_parser.sv $R/hdl/ieee1722/avtp/KL_stream_table.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv $R/hdl/ieee1722/crf/KL_crf_rx.sv $R/hdl/ieee1722/crf/KL_crf_tx.sv $R/hdl/ieee1722/maap/KL_maap.sv $R/hdl/ieee1722/aaf/KL_i2s_playback.sv $R/hdl/ieee1722/aaf/KL_i2s_feed_mux.sv $R/hdl/ieee1722/aaf/KL_tone_gen.sv $R/hdl/ieee1722/aaf/KL_media_adv.sv $C/cdc_pair_fifo.sv $R/hdl/ieee1722/aaf/KL_pcm_route.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv $R/hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv $R/hdl/ieee1722/aaf/KL_tdm_capture.sv $R/hdl/ieee1722/aaf/KL_aaf_packetizer.sv $R/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv $R/hdl/ieee1722/aaf/KL_aaf_latency_taps.sv $R/hdl/ieee1722/aaf/KL_chan_map_capture.sv $R/hdl/ieee1722/aaf/KL_chan_map_render.sv $R/hdl/ieee1722/aaf/KL_pcm_tx.sv $R/hdl/ieee1722/aaf/KL_tdm_render.sv $R/hdl/milan/milan_datapath.sv"

# The area-relevant tops: the four zero-BRAM LUT hogs of the placer-overflow
# report, their parents, and the crf_rx precedent for calibration.
tops=(
  "KL_aecp_response_builder|$C/ethernet_packet_pkg.sv $D/adp_pkg.sv $K/aecp_pkg.sv $K/KL_aecp_aem_store.sv $K/KL_aecp_aem_dyn_mux.sv $K/KL_aecp_response_builder.sv"
  "KL_lwsrp_walker|$S/lwsrp_pkg.sv $S/KL_lwsrp_walker.sv"
  "KL_acmp_lstn_ctx|$M/acmp_pkg.sv $M/KL_acmp_lstn_ctx.sv"
  "KL_acmp_tlkr_ctx|$M/acmp_pkg.sv $M/KL_acmp_tlkr_ctx.sv"
  "KL_chan_map_render|$R/hdl/ieee1722/aaf/KL_chan_map_render.sv"
  "KL_crf_rx|$R/hdl/ieee1722/crf/KL_crf_rx.sv"
  "KL_acmp_listener|$M/acmp_pkg.sv $M/KL_acmp_lstn_ctx.sv $M/KL_acmp_listener.sv"
  "KL_lwsrp_rx|$S/lwsrp_pkg.sv $S/KL_lwsrp_walker.sv $S/KL_lwsrp_registrar.sv $S/KL_lwsrp_ta_registrar.sv $S/KL_lwsrp_rx.sv"
  "KL_aecp_top|$C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $D/adp_pkg.sv $A/axis_fifo.v $AECP_SRCS"
  "KL_lwsrp_top|$A/axis_fifo.v $LWSRP_SRCS"
  "milan_datapath|$DP_SRCS"
)

want=("$@")
printf "== OOC area (synth_xilinx -family xc7 -flatten) ==\n"
printf "%-28s %8s %8s %8s %8s %8s\n" top LUT FF RAMB36 RAMB18 DSP
for spec in "${tops[@]}"; do
  top="${spec%%|*}"; srcs="${spec#*|}"
  if [ ${#want[@]} -gt 0 ]; then
    hit=0; for w in "${want[@]}"; do [ "$w" = "$top" ] && hit=1; done
    [ $hit -eq 1 ] || continue
  fi
  if ! sv2v --top="$top" $INC $srcs > "$TMP/$top.ooc.v" 2> "$TMP/$top.ooc.sv2v.err"; then
    printf "%-28s sv2v FAIL: %s\n" "$top" "$(head -1 "$TMP/$top.ooc.sv2v.err")"; continue
  fi
  # OOC_CHPARAM="N_STREAMS=8 AUDIO_IF_SLOTS_P=16 ..." elaborates the SHIP
  # shape instead of the SV defaults (milan_datapath defaults N_STREAMS=1,
  # which constant-folds the NxN engines away and reads as a fake win).
  chp=""
  for kv in ${OOC_CHPARAM:-}; do chp="$chp chparam -set ${kv%%=*} ${kv#*=} $top;"; done
  yosys -p "read_verilog $TMP/$top.ooc.v;$chp synth_xilinx -family xc7 -top $top -flatten; stat; write_json $TMP/$top.ooc.json" \
    > "$TMP/$top.ooc.log" 2>&1
  if [ $? -ne 0 ]; then
    printf "%-28s yosys FAIL: %s\n" "$top" "$(grep -iE '^ERROR' "$TMP/$top.ooc.log" | head -1)"; continue
  fi
  # count from the final (post-flatten) `stat` block only. yosys prints
  # "<count>   <CELLTYPE>", so the count is $1 and the type is $2.
  awk -v top="$top" '
    /^=== .* ===$/ { inblk = 0 }
    $0 == "=== " top " ===" { inblk = 1; lut=0; ff=0; r36=0; r18=0; dsp=0 }
    inblk && $2 ~ /^LUT[1-6]$/     { lut += $1 }
    inblk && $2 ~ /^FD[CPRS]E?$/   { ff  += $1 }
    inblk && $2 ~ /^RAMB36E1$/     { r36 += $1 }
    inblk && $2 ~ /^RAMB18E1$/     { r18 += $1 }
    inblk && $2 ~ /^DSP48E1$/      { dsp += $1 }
    END { printf "%-28s %8d %8d %8d %8d %8d\n", top, lut, ff, r36, r18, dsp }
  ' "$TMP/$top.ooc.log"
done
[ -n "${OOC_TMP:-}" ] || rm -rf "$TMP"
