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
E="$R/hdl/common/eth_event_counter"; D="$R/hdl/ieee17221/adp"
F="$R/hdl/ieee8021q/filtering"
INC="-DSYNTHESIS -I $R/hdl/common -I $R/hdl/common/csr -I $Q -I $E -I $D -I $P"
SYNTH="${YOSYS_SYNTH:-synth}"           # generic 'synth' = device-independent
TMP="$(mktemp -d)"

# THE PROTOCOL PROCESSOR IS THE CONTROL PLANE (scenario B, 2026-08-13). It used
# to be a shadow plane behind PP_PLANE_P, which is why this list was once an
# ISLAND: the datapath did not instantiate it, and the submodule's
# adp_pkg/acmp_pkg would have collided with this repository's same-named
# packages in one compilation unit. Both reasons are gone - the legacy
# 1722.1/SRP plane is deleted, the submodule's packages are namespaced
# pp_adp_pkg/pp_acmp_pkg, and milan_datapath instantiates KL_pp_shadow
# unconditionally - so this variable now feeds BOTH the standalone KL_pp_shadow
# top and the milan_datapath entry. Packages first: their importers follow.
# Order mirrors tb/verilator/milan_dp/Makefile's PP_SRCS.
PP="$R/protocol-processor/hdl"
PP_SRCS="$PP/common/pp_pkg.sv $PP/srp/srp_pkg.sv $PP/acmp/pp_acmp_pkg.sv $PP/adp/pp_adp_pkg.sv $PP/common/KL_pp_prng.sv $PP/common/KL_pp_timer_service.sv $PP/packet_engine/KL_pp_rx_validator.sv $PP/packet_engine/KL_pp_rx_slots.sv $PP/packet_engine/KL_pp_normalizer.sv $PP/packet_engine/KL_pp_dispatch.sv $PP/packet_engine/KL_pp_tx_slots.sv $PP/packet_engine/KL_pp_tx_arbiter.sv $PP/packet_engine/KL_pp_scoreboard.sv $PP/packet_engine/KL_pp_event_router.sv $PP/packet_engine/KL_pp_originator.sv $PP/packet_engine/KL_pp_trace_ring.sv $PP/packet_engine/KL_pp_side_port.sv $PP/packet_engine/KL_pp_nvm_port.sv $PP/adp/KL_adp_engine.sv $PP/acmp/KL_pp_acmp_listener.sv $PP/acmp/KL_acmp_talker.sv $PP/acmp/KL_acmp_nvm_shadow.sv $PP/srp/KL_srp_decoder.sv $PP/srp/KL_srp_domain.sv $PP/srp/KL_srp_vlan.sv $PP/srp/KL_srp_admission.sv $PP/srp/KL_srp_talker_fsm.sv $PP/srp/KL_srp_listener_fsm.sv $PP/srp/KL_srp_encoder.sv $PP/srp/KL_srp_top.sv $PP/aecp/ucpu_pkg.sv $PP/aecp/KL_aecp_ucpu.sv $PP/aecp/KL_aecp_desc_store.sv $PP/aecp/KL_aecp_engine.sv $PP/top/KL_mrp_strip.sv $PP/top/protocol_processor_top.sv $R/hdl/milan/KL_pp_shadow.sv $R/hdl/milan/KL_pp_maap_shim.sv"

for t in sv2v yosys; do command -v $t >/dev/null || { echo "missing tool: $t (see syn/yosys/README.md)"; exit 2; }; done

# protocol_processor_top $readmemh's its ACMP transition ROM by a RELATIVE
# name, and yosys resolves that against ITS OWN working directory - not against
# the source file. Without this the KL_pp_shadow top dies with
# "Can not open file `ltn_rom.hex` for $readmemh" and, because that is not an
# "^ERROR"-prefixed line this script greps for, it reports a FAIL with an EMPTY
# reason. Generate the image where yosys will look for it.
# It lands in the CURRENT directory on purpose: that is what yosys inherits,
# whichever directory this script was invoked from.
if [ -f "$R/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py" ]; then
  python3 "$R/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py" -o ltn_rom.hex >/dev/null 2>&1 || true
fi
# ...and the AECP uCPU microcode image, same relative-$readmemh contract.
if [ -f "$R/protocol-processor/hdl/aecp/ucode/gen_ucode.py" ]; then
  python3 "$R/protocol-processor/hdl/aecp/ucode/gen_ucode.py" -o ucode.hex >/dev/null 2>&1 || true
fi

# top | source files (interface modules go through their flat wrapper)
tops=(
  "tcam|$F/tcam.sv"
  "cdc_pulse|$C/cdc_pulse.sv"
  "cdc_handshake|$C/cdc_handshake.sv"
  "adp_tx_arbiter|$D/adp_tx_arbiter.sv"
  "rx_mac_filter|$F/tcam.sv $F/rx_mac_filter.sv $C/tx_ifg_gasket.sv"
  "milan_csr|$R/hdl/common/csr/milan_csr.sv"
  "KL_avtp_rx_monitor|$R/hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv"
  "KL_stream_table|$R/hdl/ieee1722/avtp/KL_stream_table.sv"
  "avtp_stream_parser|$C/ethernet_packet_pkg.sv $R/hdl/ieee1722/avtp/avtp_subtype_pkg.sv $R/hdl/ieee1722/avtp/avtp_stream_parser.sv"
  "KL_avtp_rx_monitor_ctx|$R/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
  "KL_pcm_route|$R/hdl/ieee1722/aaf/KL_pcm_route.sv"
  "KL_aaf_capture_i2s|$C/cdc_pair_fifo.sv $R/hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv"
  "KL_tdm_capture|$C/cdc_pair_fifo.sv $R/hdl/ieee1722/aaf/KL_tdm_capture.sv"
  "KL_aes3_rx|$C/cdc_pair_fifo.sv $C/cdc_pulse.sv $R/hdl/ieee1722/aaf/KL_aes3_rx.sv"
  "KL_aes3_tx|$C/cdc_pair_fifo.sv $C/cdc_pulse.sv $R/hdl/ieee1722/aaf/KL_aes3_tx.sv"
  "KL_aaf_packetizer|$R/hdl/ieee1722/aaf/KL_aaf_packetizer.sv"
  "KL_crf_rx|$R/hdl/ieee1722/crf/KL_crf_rx.sv"
  "KL_crf_tx|$C/cdc_pulse.sv $R/hdl/ieee1722/crf/KL_crf_tx.sv"
  "KL_mmcm_drp_servo|$C/cdc_pulse.sv $C/cdc_handshake.sv $R/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"
  "KL_media_nco|$R/hdl/ieee1722/crf/KL_media_nco.sv"
  "KL_link_guard|$C/KL_link_guard.sv"
  "KL_maap|$R/hdl/ieee1722/maap/KL_maap.sv"
  "KL_i2s_playback|$C/cdc_pair_fifo.sv $C/cdc_pulse.sv $R/hdl/ieee1722/aaf/KL_i2s_playback.sv"
  "KL_i2s_feed_mux|$R/hdl/ieee1722/aaf/KL_i2s_feed_mux.sv"
  "KL_chan_map_render|$R/hdl/ieee1722/aaf/KL_chan_map_render.sv"
  # capture mux OOC: it was only ever synthesised inside milan_datapath, so
  # nothing gated it standalone - and since the rx->talker loopback it has
  # DEFAULT PORT VALUES on its optional pins, which sv2v must lower into
  # call-site localparams for yosys to see a constant rather than a dangling
  # wire. That lowering is exactly the kind of thing a full-datapath synth
  # hides behind a driven net.
  "KL_chan_map_capture|$R/hdl/ieee1722/aaf/KL_chan_map_capture.sv"
  "KL_pcm_tx|$R/hdl/ieee1722/aaf/KL_pcm_tx.sv"
  "KL_tone_gen|$R/hdl/ieee1722/aaf/KL_tone_gen.sv"
  "KL_aaf_rx_depacketizer|$A/axis_fifo.v $R/hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv"
  "credit_based_shaper|$C/ethernet_packet_pkg.sv $Q/credit_based_shaper.sv"
  "timestamp_counter|$P/timestamp_counter.sv"
  "KL_ptp_clock_validity|$P/KL_ptp_clock_validity.sv"
  "ptp_csr_sync|$P/ptp_csr_sync.sv"
  "event_counter|$E/event_counter.sv"
  "ethernet_events|$E/ethernet_events.sv $E/event_counter.sv"
  "KL_mac_rmon_events|$C/cdc_pulse.sv $E/KL_mac_rmon_events.sv"
  "classifier_wrap|$C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $Q/traffic_class_map.sv $Q/traffic_classifier.sv $A/axis_fifo.v $R/tb/verilator/classifier/classifier_wrap.sv"
  "queues_wrap|$C/axi_stream_if.sv $Q/traffic_queues.sv $A/axis_fifo.v $A/axis_demux.v $A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v $R/tb/verilator/queues/queues_wrap.sv"
  "KL_pp_shadow|$A/axis_fifo.v $PP_SRCS"
  # KL_maap claims a BLOCK, the processor asks PER SOURCE; this is the adapter.
  # Standalone by design - it has no dependency on either side's sources, which
  # is the whole point of it being its own file rather than glue inside
  # KL_pp_shadow: it can be synthesised, read and reasoned about on its own.
  "KL_pp_maap_shim|$R/hdl/milan/KL_pp_maap_shim.sv"
  "axis_fifo|$A/axis_fifo.v"
  "axis_demux|$A/axis_demux.v"
  "axis_arb_mux|$A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v"
  "milan_datapath|$PP_SRCS $C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $A/axis_fifo.v $A/axis_demux.v $A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v $Q/traffic_class_map.sv $Q/traffic_classifier.sv $Q/credit_based_shaper.sv $Q/traffic_shaping_core.sv $Q/traffic_queues.sv $Q/traffic_controller_802_1q.sv $P/timestamp_counter.sv $P/ptp_csr_sync.sv $C/cdc_pulse.sv $C/cdc_handshake.sv $C/axis_mux_rr_2in_1out.sv $P/ptp_ts_core.sv $P/ptp_ts_top.sv $P/KL_ptp_clock_validity.sv $F/tcam.sv $F/rx_mac_filter.sv $C/tx_ifg_gasket.sv $R/hdl/ieee1722/aaf/KL_pcm_lpf.sv $C/KL_link_guard.sv $D/adp_tx_arbiter.sv $E/ethernet_events.sv $E/event_counter.sv $R/hdl/common/csr/milan_csr.sv $R/hdl/ieee1722/aaf/aaf_talker_i2s.sv $R/hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv $R/hdl/ieee1722/avtp/avtp_subtype_pkg.sv $R/hdl/ieee1722/avtp/avtp_stream_parser.sv $R/hdl/ieee1722/avtp/KL_stream_table.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv $R/hdl/ieee1722/crf/KL_crf_rx.sv $R/hdl/ieee1722/crf/KL_crf_tx.sv $R/hdl/ieee1722/maap/KL_maap.sv $R/hdl/ieee1722/aaf/KL_i2s_playback.sv $R/hdl/ieee1722/aaf/KL_i2s_feed_mux.sv $R/hdl/ieee1722/aaf/KL_tone_gen.sv $R/hdl/ieee1722/aaf/KL_media_adv.sv $C/cdc_pair_fifo.sv $R/hdl/ieee1722/aaf/KL_pcm_route.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv $R/hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv $R/hdl/ieee1722/aaf/KL_tdm_capture.sv $R/hdl/ieee1722/aaf/KL_aaf_packetizer.sv $R/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv $R/hdl/ieee1722/crf/KL_media_nco.sv $R/hdl/ieee1722/aaf/KL_aaf_latency_taps.sv $R/hdl/ieee1722/aaf/KL_chan_map_capture.sv $R/hdl/ieee1722/aaf/KL_chan_map_render.sv $R/hdl/ieee1722/aaf/KL_pcm_tx.sv $R/hdl/ieee1722/aaf/KL_tdm_render.sv $R/hdl/ieee1722/avtp/KL_media_clock_restart.sv $R/hdl/ieee1722/avtp/KL_talker_diag_ctx.sv $R/hdl/ieee1722/aaf/KL_pair_blend.sv $R/hdl/ieee1722/aaf/KL_pair_zero_fill.sv $R/hdl/ieee1722/aaf/KL_tdm_capture_master.sv $R/hdl/milan/milan_datapath.sv"
)

echo "== Yosys open-synthesis check ($SYNTH, via sv2v) =="
pass=0; fail=0
for spec in "${tops[@]}"; do
  top="${spec%%|*}"; srcs="${spec#*|}"
  # SHAPE INCLUDE (2026-08-03). milan_datapath includes gen/adp_shape_defaults.svh
  # and $errors when ADP_TALKER_SRC_C is neither N_STREAMS nor N_STREAMS+1. The
  # TRACKED copy under hdl/common/csr is whichever config last ran
  # endstation_builder.py --write-rtl - today the AX7101 8x8 shape, so
  # ADP_TALKER_SRC_C=9 - while this gate elaborates every top at its DEFAULT
  # parameters, i.e. N_STREAMS=1. That mismatch is not a defect in either place;
  # it is the guard doing its job, and it had this gate stuck at 48/49 for every
  # lane, which is how a permanently-red gate stops being read at all.
  # Prepending the N_STREAMS=1 config resolves the include to a MATCHING shape
  # (the guard's own message prescribes exactly this), and it must come BEFORE
  # hdl/common/csr on the path to win. Elaborating at the 8x8 shape instead
  # would need a parameter override sv2v does not take here.
  inc="$INC"
  [ "$top" = "milan_datapath" ] && \
    inc="-I $R/configs/generated/endstation_arty_current $INC"
  if ! sv2v --top="$top" $inc $srcs > "$TMP/$top.v" 2> "$TMP/$top.sv2v.err"; then
    printf "  [FAIL] %-22s sv2v: %s\n" "$top" "$(head -1 "$TMP/$top.sv2v.err")"; fail=$((fail+1)); continue
  fi
  # stat -top + the design-hierarchy total: plain `stat` prints one block per
  # module and `head -1` picked whichever leaf came first (tcam), so the cells=
  # column reported that leaf for every top rather than the design.
  yosys -p "read_verilog $TMP/$top.v; $SYNTH -top $top; hierarchy -check; stat -top $top" > "$TMP/$top.yos.log" 2>&1
  rc=$?
  cells="$(awk '/=== design hierarchy ===/{f=1} f && /^[[:space:]]+[0-9]+ cells$/{print $1; exit}' "$TMP/$top.yos.log")"
  if [ $rc -eq 0 ]; then printf "  [PASS] %-22s cells=%s\n" "$top" "${cells:-?}"; pass=$((pass+1))
  else printf "  [FAIL] %-22s yosys: %s\n" "$top" "$(grep -iE '^ERROR' "$TMP/$top.yos.log" | head -1)"; fail=$((fail+1)); fi
done
echo "--------------------------------------------------------------"
echo "tops: $((pass+fail))   pass: $pass   fail: $fail"
echo "RESULT: $([ $fail -eq 0 ] && echo PASS || echo FAIL)"
rm -rf "$TMP"
# STRUCTURAL GATE (the RMON tied-bus class): inventory of milan_datapath
# inputs the SoC instantiation ties to constants, so a green port-level TB can
# never again silently vouch for a cone silicon never drives. Since 2026-07-26
# this FAILS the run on a never-overridden tie that carries no justified-tie
# entry - it was informational-only while three of its four warnings were
# expected, which is precisely why the fourth (dead RMON) went unread.
tie_fail=0
"$R/scripts/check_tied_inputs.sh" || tie_fail=1
# Observer-purity structural report (the host-plane regression class,
# 2026-07-25): taps/telemetry must never drive the observed streams' nets.
# Reported here like the tied-input inventory (never changes this script's
# RESULT); standalone syn/yosys/check_tap_purity.sh is the exit-coded gate.
"$R/syn/yosys/check_tap_purity.sh" || true
[ $tie_fail -eq 0 ] || echo "RESULT: FAIL (tied-input gate)"
[ $fail -eq 0 ] && [ $tie_fail -eq 0 ]
