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
E="$R/hdl/common/eth_event_counter"; D="$R/hdl/ieee17221/adp"
F="$R/hdl/ieee8021q/filtering"
INC="-DSYNTHESIS -I $R/hdl/common -I $R/hdl/common/csr -I $Q -I $E -I $D -I $P"
TMP="${OOC_TMP:-$(mktemp -d)}"; mkdir -p "$TMP"

# The protocol processor is the control plane (scenario B): milan_datapath
# instantiates KL_pp_shadow unconditionally, so its sources are datapath
# sources and belong in DP_SRCS. Packages first.
PP="$R/protocol-processor/hdl"
# Derived from the submodule tree; see scripts/pp_srcs.py. The parent's own
# two files stay explicit because they are this repository's, not the
# submodule's. The status is taken rather than discarded: `$(...)` in an
# assignment drops it, and the generator's refusal to emit an empty list is
# worth nothing on this side of the process boundary if nobody reads it.
PP_DERIVED="$(python3 "$R/scripts/pp_srcs.py" --prefix "$PP")" || exit 2
PP_SRCS="$PP_DERIVED $R/hdl/milan/KL_pp_shadow.sv $R/hdl/milan/KL_pp_maap_shim.sv"

# ...and with the processor comes its ROM. protocol_processor_top $readmemh's
# the ACMP listener transition image by the RELATIVE name "ltn_rom.hex", which
# yosys resolves against ITS OWN working directory, not against the source
# file. Generate it where yosys will look (syn/yosys/run.sh does the same, and
# for the same reason - without it the top dies on a file-open error).
if [ -f "$R/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py" ]; then
  python3 "$R/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py" -o ltn_rom.hex >/dev/null 2>&1 || true
fi

DP_SRCS="$PP_SRCS $C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $A/axis_fifo.v $A/axis_demux.v $A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v $Q/traffic_class_map.sv $Q/traffic_classifier.sv $Q/credit_based_shaper.sv $Q/traffic_shaping_core.sv $Q/traffic_queues.sv $Q/traffic_controller_802_1q.sv $P/timestamp_counter.sv $P/ptp_csr_sync.sv $C/cdc_pulse.sv $C/cdc_handshake.sv $C/axis_mux_rr_2in_1out.sv $P/ptp_ts_core.sv $P/ptp_ts_top.sv $F/tcam.sv $F/rx_mac_filter.sv $C/tx_ifg_gasket.sv $R/hdl/ieee1722/aaf/KL_pcm_lpf.sv $C/KL_link_guard.sv $D/adp_tx_arbiter.sv $E/ethernet_events.sv $E/event_counter.sv $R/hdl/common/csr/milan_csr.sv $R/hdl/ieee1722/aaf/aaf_talker_i2s.sv $R/hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv $R/hdl/ieee1722/avtp/avtp_subtype_pkg.sv $R/hdl/ieee1722/avtp/avtp_stream_parser.sv $R/hdl/ieee1722/avtp/KL_stream_table.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv $R/hdl/ieee1722/crf/KL_crf_rx.sv $R/hdl/ieee1722/crf/KL_crf_tx.sv $R/hdl/ieee1722/maap/KL_maap.sv $R/hdl/ieee1722/aaf/KL_i2s_playback.sv $R/hdl/ieee1722/aaf/KL_i2s_feed_mux.sv $R/hdl/ieee1722/aaf/KL_tone_gen.sv $R/hdl/ieee1722/aaf/KL_media_adv.sv $C/cdc_pair_fifo.sv $R/hdl/ieee1722/aaf/KL_pcm_route.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv $R/hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv $R/hdl/ieee1722/aaf/KL_tdm_capture.sv $R/hdl/ieee1722/aaf/KL_aaf_packetizer.sv $R/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv $R/hdl/ieee1722/crf/KL_media_nco.sv $R/hdl/ieee1722/aaf/KL_aaf_latency_taps.sv $R/hdl/ieee1722/aaf/KL_chan_map_capture.sv $R/hdl/ieee1722/aaf/KL_chan_map_render.sv $R/hdl/ieee1722/aaf/KL_pcm_tx.sv $R/hdl/ieee1722/aaf/KL_tdm_render.sv $R/hdl/milan/milan_datapath.sv $R/hdl/ieee1722/aaf/KL_tdm_capture_master.sv $R/hdl/ieee1722/aaf/KL_pair_blend.sv $R/hdl/ieee1722/aaf/KL_pair_zero_fill.sv $R/hdl/ieee1722/avtp/KL_talker_diag_ctx.sv $R/hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv"

# The area-relevant tops: the zero-BRAM LUT hogs of the placer-overflow report,
# their parents, and the crf_rx precedent for calibration.
#
# THE 1722.1/SRP ENTRIES ARE GONE, not moved. KL_aecp_response_builder,
# KL_aem_patch, KL_aecp_top, KL_lwsrp_walker/_rx/_top and the two ACMP contexts
# were the biggest names on this list and every one of them measured RTL that
# no longer exists - the protocol processor replaced that whole plane. Its own
# area is measured as KL_pp_shadow (syn/yosys/run.sh has the elaboration) and
# inside milan_datapath below, which is the number that decides placement.
tops=(
  "KL_chan_map_render|$R/hdl/ieee1722/aaf/KL_chan_map_render.sv"
  "KL_chan_map_capture|$R/hdl/ieee1722/aaf/KL_chan_map_capture.sv"
  "KL_crf_rx|$R/hdl/ieee1722/crf/KL_crf_rx.sv"
  "KL_pp_shadow|$A/axis_fifo.v $PP_SRCS"
  # docs/design/AREA_BUDGET.md tier-1 optional blocks, each measured ALONE so
  # its prune parameter can be priced against a standalone figure as well as
  # against the milan_datapath delta. Standalone OOC is the UPPER bound for a
  # prune: in context the block shares decode and constants with its
  # neighbours, so the datapath delta is always the smaller (and truer) number.
  "KL_mmcm_drp_servo|$C/cdc_pulse.sv $C/cdc_handshake.sv $R/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"
  "KL_aaf_latency_taps|$R/hdl/ieee1722/aaf/KL_aaf_latency_taps.sv"
  "KL_maap|$R/hdl/ieee1722/maap/KL_maap.sv"
  "KL_i2s_playback|$C/cdc_pulse.sv $C/cdc_pair_fifo.sv $R/hdl/ieee1722/aaf/KL_i2s_playback.sv"
  "rx_mac_filter|$F/tcam.sv $F/rx_mac_filter.sv"
  "tcam|$F/tcam.sv"
  "KL_pcm_lpf|$R/hdl/ieee1722/aaf/KL_pcm_lpf.sv"
  "milan_datapath|$DP_SRCS"
)

want=("$@")
printf "== OOC area (synth_xilinx -family xc7 -flatten) ==\n"
printf "%-28s %8s %8s %8s %8s %8s %8s\n" top LUT FF RAMB36 RAMB18 DSP CARRY4
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
  #
  # KNOWN LIMIT (2026-07-27): `chparam` does NOT work on the milan_datapath
  # top. It re-derives the module, which re-runs the AST frontend over sv2v's
  # flattened interface names and dies with
  #   ERROR: Failed to detect width for identifier
  #          \traffic_controller.buffer_queues.…tdest
  # It works fine on the leaf tops. To shape milan_datapath, patch the SV
  # DEFAULT in a private copy of hdl/milan/milan_datapath.sv and point this
  # script's source list at it - equivalent, since the parameter IS its
  # default in any build that does not override it (recipe and the numbers it
  # produced: docs/design/AREA_BUDGET.md).
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
    $0 == "=== " top " ===" { inblk = 1; lut=0; ff=0; r36=0; r18=0; dsp=0; c4=0 }
    inblk && $2 ~ /^LUT[1-6]$/     { lut += $1 }
    inblk && $2 ~ /^FD[CPRS]E?$/   { ff  += $1 }
    inblk && $2 ~ /^RAMB36E1$/     { r36 += $1 }
    inblk && $2 ~ /^RAMB18E1$/     { r18 += $1 }
    inblk && $2 ~ /^DSP48E1$/      { dsp += $1 }
    inblk && $2 ~ /^CARRY4$/       { c4  += $1 }
    END { printf "%-28s %8d %8d %8d %8d %8d %8d\n", top, lut, ff, r36, r18, dsp, c4 }
  ' "$TMP/$top.ooc.log"
done
[ -n "${OOC_TMP:-}" ] || rm -rf "$TMP"
