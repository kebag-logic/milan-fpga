#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Open-toolchain synthesis check: prove the (XPM-free) RTL maps to a generic,
# device-independent cell library with Yosys. SystemVerilog is lowered by sv2v.
#
#   ./run.sh                                  # full serial gate, every top
#   ./run.sh --list                           # print the authoritative inventory
#   ./run.sh --shard 0/4 --results out/       # one weighted CI worker
#   ./run.sh --mode elaborate --top TOP       # fast hierarchy/process smoke
#   YOSYS_SYNTH=synth_ecp5 ./run.sh           # target a real device
#
# Requires yosys and sv2v except for --list.

set -u

usage() {
  cat <<'EOF'
usage: syn/yosys/run.sh [options]

  --shard INDEX/TOTAL    select one deterministic weighted shard (default 0/1)
  --top NAME             select one explicit top; may be repeated
  --list                 print selected top names without requiring tools
  --mode full|elaborate  full synthesis or fast hierarchy/process smoke
  --results DIRECTORY    write one machine-readable result per top/gate
  --no-structural        do not run the tied-input and tap-purity checks
  -h, --help             show this help
EOF
}

SHARD="0/1"
MODE="full"
LIST=0
RESULTS=""
NO_STRUCTURAL=0
REQUESTED_TOPS=()
while [ "$#" -gt 0 ]; do
  case "$1" in
    --shard)
      [ "$#" -ge 2 ] || { echo "--shard needs INDEX/TOTAL" >&2; exit 2; }
      SHARD="$2"; shift 2 ;;
    --shard=*) SHARD="${1#--shard=}"; shift ;;
    --top)
      [ "$#" -ge 2 ] || { echo "--top needs NAME" >&2; exit 2; }
      REQUESTED_TOPS+=("$2"); shift 2 ;;
    --top=*) REQUESTED_TOPS+=("${1#--top=}"); shift ;;
    --mode)
      [ "$#" -ge 2 ] || { echo "--mode needs full or elaborate" >&2; exit 2; }
      MODE="$2"; shift 2 ;;
    --mode=*) MODE="${1#--mode=}"; shift ;;
    --results)
      [ "$#" -ge 2 ] || { echo "--results needs DIRECTORY" >&2; exit 2; }
      RESULTS="$2"; shift 2 ;;
    --results=*) RESULTS="${1#--results=}"; shift ;;
    --list) LIST=1; shift ;;
    --no-structural) NO_STRUCTURAL=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done
case "$MODE" in
  full|elaborate) ;;
  *) echo "--mode must be full or elaborate" >&2; exit 2 ;;
esac
if [ "${#REQUESTED_TOPS[@]}" -gt 0 ] && [ "$SHARD" != "0/1" ]; then
  echo "--top and a non-default --shard are mutually exclusive" >&2
  exit 2
fi

export PATH="$HOME/.local/bin:$PATH"
R="$(cd "$(dirname "$0")/../.." && pwd)"
A="$R/third_party/verilog-axis/rtl"
C="$R/hdl/common"; Q="$R/hdl/ieee8021q/ts"; P="$R/hdl/ieee8021as/ptp_timestamp"
E="$R/hdl/common/eth_event_counter"; D="$R/hdl/ieee17221/adp"
F="$R/hdl/ieee8021q/filtering"
INC="-DSYNTHESIS -I $R/hdl/common -I $R/hdl/common/csr -I $Q -I $E -I $D -I $P"
SYNTH="${YOSYS_SYNTH:-synth}"

# THE PROTOCOL PROCESSOR IS THE CONTROL PLANE (scenario B, 2026-08-13).
# The source list is derived from the checked-out submodule. Take the generator
# status explicitly: command substitution in an assignment otherwise hides a
# refusal and an empty source list can elaborate a meaningless shadow wrapper.
PP="$R/protocol-processor/hdl"
command -v python3 >/dev/null || {
  echo "missing tool: python3 (required by scripts/pp_srcs.py)" >&2
  exit 2
}
PP_DERIVED="$(python3 "$R/scripts/pp_srcs.py" --prefix "$PP")" || exit 2
PP_SRCS="$PP_DERIVED $R/hdl/milan/KL_pp_shadow.sv $R/hdl/milan/KL_pp_maap_shim.sv"

# top | source files (interface modules go through their flat wrapper)
tops=(
  "tcam|$F/tcam.sv"
  "cdc_pulse|$C/cdc_pulse.sv"
  "cdc_handshake|$C/cdc_handshake.sv"
  "adp_tx_arbiter|$D/adp_tx_arbiter.sv"
  "rx_mac_filter|$F/tcam.sv $F/rx_mac_filter.sv $C/tx_ifg_gasket.sv"
  "milan_csr|$R/hdl/common/csr/milan_csr.sv"
  "KL_gptp_txstamp|$R/hdl/ieee8021as/gptp_plane/KL_gptp_txstamp.sv"
  "KL_gptp_shadow|$R/gptp-processor/hdl/ucpu/gptp_ucpu_pkg.sv $R/gptp-processor/hdl/ucpu/KL_gptp_ucpu.sv $R/gptp-processor/hdl/wire/KL_gptp_rx_parser.sv $R/gptp-processor/hdl/wire/KL_gptp_tx_slot.sv $R/gptp-processor/hdl/common/KL_gptp_timer.sv $R/gptp-processor/hdl/top/KL_gptp_engine.sv $R/third_party/verilog-axis/rtl/axis_fifo.v $R/hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv"
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
  "KL_pp_maap_shim|$R/hdl/milan/KL_pp_maap_shim.sv"
  "axis_fifo|$A/axis_fifo.v"
  "axis_demux|$A/axis_demux.v"
  "axis_arb_mux|$A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v"
  "milan_datapath|$PP_SRCS $C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $A/axis_fifo.v $A/axis_demux.v $A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v $Q/traffic_class_map.sv $Q/traffic_classifier.sv $Q/credit_based_shaper.sv $Q/traffic_shaping_core.sv $Q/traffic_queues.sv $Q/traffic_controller_802_1q.sv $P/timestamp_counter.sv $P/ptp_csr_sync.sv $C/cdc_pulse.sv $C/cdc_handshake.sv $C/axis_mux_rr_2in_1out.sv $P/ptp_ts_core.sv $P/ptp_ts_top.sv $P/KL_ptp_clock_validity.sv $F/tcam.sv $F/rx_mac_filter.sv $C/tx_ifg_gasket.sv $R/hdl/ieee1722/aaf/KL_pcm_lpf.sv $C/KL_link_guard.sv $D/adp_tx_arbiter.sv $E/ethernet_events.sv $E/event_counter.sv $R/hdl/common/csr/milan_csr.sv $R/hdl/ieee1722/aaf/aaf_talker_i2s.sv $R/hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv $R/hdl/ieee1722/avtp/avtp_subtype_pkg.sv $R/hdl/ieee1722/avtp/avtp_stream_parser.sv $R/hdl/ieee1722/avtp/KL_stream_table.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv $R/hdl/ieee1722/crf/KL_crf_rx.sv $R/hdl/ieee1722/crf/KL_crf_tx.sv $R/hdl/ieee1722/maap/KL_maap.sv $R/hdl/ieee1722/aaf/KL_i2s_playback.sv $R/hdl/ieee1722/aaf/KL_i2s_feed_mux.sv $R/hdl/ieee1722/aaf/KL_tone_gen.sv $R/hdl/ieee1722/aaf/KL_media_adv.sv $C/cdc_pair_fifo.sv $R/hdl/ieee1722/aaf/KL_pcm_route.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv $R/hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv $R/hdl/ieee1722/aaf/KL_tdm_capture.sv $R/hdl/ieee1722/aaf/KL_aaf_packetizer.sv $R/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv $R/hdl/ieee1722/crf/KL_media_nco.sv $R/hdl/ieee1722/aaf/KL_aaf_latency_taps.sv $R/hdl/ieee1722/aaf/KL_chan_map_capture.sv $R/hdl/ieee1722/aaf/KL_chan_map_render.sv $R/hdl/ieee1722/aaf/KL_pcm_tx.sv $R/hdl/ieee1722/aaf/KL_tdm_render.sv $R/hdl/ieee1722/avtp/KL_media_clock_restart.sv $R/hdl/ieee1722/avtp/KL_talker_diag_ctx.sv $R/hdl/ieee1722/aaf/KL_pair_blend.sv $R/hdl/ieee1722/aaf/KL_pair_zero_fill.sv $R/hdl/ieee1722/aaf/KL_tdm_capture_master.sv $R/hdl/milan/milan_datapath.sv"
)

all_names=()
declare -A spec_by_name=()
for spec in "${tops[@]}"; do
  name="${spec%%|*}"
  if [ "${spec_by_name[$name]+set}" = set ]; then
    echo "duplicate top in inventory: $name" >&2
    exit 2
  fi
  all_names+=("$name")
  spec_by_name[$name]="$spec"
done

python3 "$R/scripts/yosys_shards.py" --selftest >/dev/null || {
  echo "Yosys shard selector fails its own self-test" >&2
  exit 2
}

selected_names=()
if [ "${#REQUESTED_TOPS[@]}" -gt 0 ]; then
  declare -A requested_seen=()
  for name in "${REQUESTED_TOPS[@]}"; do
    [ "${spec_by_name[$name]+set}" = set ] || {
      echo "unknown top: $name" >&2
      exit 2
    }
    [ "${requested_seen[$name]+set}" != set ] || {
      echo "duplicate --top: $name" >&2
      exit 2
    }
    requested_seen[$name]=1
    selected_names+=("$name")
  done
  shard_index=0
  shard_total=1
else
  if ! selected_out=$(printf '%s\n' "${all_names[@]}" | \
      python3 "$R/scripts/yosys_shards.py" --shard "$SHARD" 2>&1); then
    echo "$selected_out" >&2
    exit 2
  fi
  while IFS= read -r name; do
    [ -n "$name" ] && selected_names+=("$name")
  done <<< "$selected_out"
  shard_index="${SHARD%%/*}"
  shard_total="${SHARD#*/}"
fi

[ "${#selected_names[@]}" -gt 0 ] || {
  echo "selected Yosys shard owns no tops" >&2
  exit 2
}

if [ "$LIST" -eq 1 ]; then
  printf '%s\n' "${selected_names[@]}"
  exit 0
fi

for tool in sv2v yosys; do
  command -v "$tool" >/dev/null || {
    echo "missing tool: $tool (see syn/yosys/README.md)" >&2
    exit 2
  }
done

[ -z "$RESULTS" ] || mkdir -p "$RESULTS"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

record_result() {
  [ -n "$RESULTS" ] || return 0
  local kind="$1" name="$2" status="$3" blocking="$4"
  local mode_value="${5:-}" cells_value="${6:-}"
  local out="$RESULTS/$kind-$name.result"
  local tmp_out="$out.tmp.$$"
  {
    printf 'kind=%s\n' "$kind"
    printf 'name=%s\n' "$name"
    printf 'status=%s\n' "$status"
    printf 'blocking=%s\n' "$blocking"
    [ -z "$mode_value" ] || printf 'mode=%s\n' "$mode_value"
    [ -z "$cells_value" ] || printf 'cells=%s\n' "$cells_value"
  } > "$tmp_out"
  mv "$tmp_out" "$out"
}

# Relative $readmemh images must exist in Yosys's working directory.
if [ -f "$R/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py" ]; then
  python3 "$R/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py" -o ltn_rom.hex >/dev/null 2>&1 || true
fi
if [ -f "$R/protocol-processor/hdl/aecp/ucode/gen_ucode.py" ]; then
  python3 "$R/protocol-processor/hdl/aecp/ucode/gen_ucode.py" -o ucode.hex >/dev/null 2>&1 || true
fi
if [ -f "$R/gptp-processor/hdl/ucode/gen_gptp_ucode.py" ]; then
  python3 "$R/gptp-processor/hdl/ucode/gen_gptp_ucode.py" -o gptp_ucode.hex >/dev/null 2>&1 || true
fi

if [ "$MODE" = full ]; then
  echo "== Yosys open-synthesis check ($SYNTH, via sv2v; shard $shard_index/$shard_total) =="
else
  echo "== Yosys fast elaboration check (via sv2v) =="
fi
pass=0
fail=0
for name in "${selected_names[@]}"; do
  spec="${spec_by_name[$name]}"
  top="${spec%%|*}"
  srcs="${spec#*|}"
  inc="$INC"
  [ "$top" = "milan_datapath" ] && \
    inc="-I $R/configs/generated/endstation_arty_current $INC"

  if ! sv2v --top="$top" $inc $srcs > "$TMP/$top.v" 2> "$TMP/$top.sv2v.err"; then
    printf "  [FAIL] %-22s sv2v: %s\n" "$top" "$(head -1 "$TMP/$top.sv2v.err")"
    record_result top "$top" FAIL 1 "$MODE" ""
    fail=$((fail + 1))
    continue
  fi

  if [ "$MODE" = full ]; then
    program="read_verilog $TMP/$top.v; $SYNTH -top $top; hierarchy -check; stat -top $top"
  else
    program="read_verilog $TMP/$top.v; hierarchy -check -top $top; proc; opt_clean; check -assert; stat -top $top"
  fi
  yosys -p "$program" > "$TMP/$top.yos.log" 2>&1
  rc=$?
  cells="$(awk '/=== design hierarchy ===/{f=1} f && /^[[:space:]]+[0-9]+ cells$/{print $1; exit}' "$TMP/$top.yos.log")"
  if [ "$rc" -eq 0 ]; then
    printf "  [PASS] %-22s cells=%s\n" "$top" "${cells:-?}"
    record_result top "$top" PASS 1 "$MODE" "${cells:-?}"
    pass=$((pass + 1))
  else
    reason="$(grep -iE '^ERROR' "$TMP/$top.yos.log" | head -1)"
    printf "  [FAIL] %-22s yosys: %s\n" "$top" "$reason"
    record_result top "$top" FAIL 1 "$MODE" "${cells:-?}"
    fail=$((fail + 1))
  fi
done

echo "--------------------------------------------------------------"
echo "tops: $((pass + fail))   pass: $pass   fail: $fail"
echo "RESULT: $([ "$fail" -eq 0 ] && echo PASS || echo FAIL)"

tie_fail=0
tap_fail=0
if [ "$NO_STRUCTURAL" -eq 0 ] && [ "$shard_index" -eq 0 ]; then
  if "$R/scripts/check_tied_inputs.sh"; then
    record_result gate tied-input PASS 1
  else
    tie_fail=1
    record_result gate tied-input FAIL 1
  fi

  # Existing policy keeps tap purity informational in this combined script;
  # its standalone script remains exit-coded. CI records the verdict exactly
  # once so a reviewer can see it without changing the local gate contract.
  if "$R/syn/yosys/check_tap_purity.sh"; then
    record_result gate tap-purity PASS 0
  else
    tap_fail=1
    record_result gate tap-purity FAIL 0
  fi
else
  echo "structural checks: skipped in this worker"
fi

[ "$tie_fail" -eq 0 ] || echo "RESULT: FAIL (tied-input gate)"
[ "$tap_fail" -eq 0 ] || echo "RESULT: NOTE (tap-purity report failed; standalone policy is informational here)"
[ "$fail" -eq 0 ] && [ "$tie_fail" -eq 0 ]
