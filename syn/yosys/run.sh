#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Open-toolchain synthesis check: prove the (XPM-free) RTL maps to a generic,
# device-independent cell library with Yosys. SystemVerilog is lowered by sv2v.
#
#   ./run.sh                                  # full serial gate, every top
#   ./run.sh --list                           # print the authoritative inventory
#   ./run.sh --emit KL_pp_shadow              # one top's record, for a consumer
#   ./run.sh --shard 0/4 --results out/       # one weighted CI worker
#   ./run.sh --mode elaborate --top TOP       # fast hierarchy/process smoke
#   YOSYS_SYNTH=synth_ecp5 ./run.sh           # target a real device
#
# Requires python3 on every path, plus yosys and sv2v except for --list, which
# needs neither those nor a checked-out submodule: it prints names only (#190).

set -u

usage() {
  cat <<'EOF'
usage: syn/yosys/run.sh [options]

  --shard INDEX/TOTAL    select one deterministic weighted shard (default 0/1)
  --top NAME             select one explicit top; may be repeated
  --list                 print selected top names; python3 only, no sv2v,
                         yosys or submodule checkout
  --emit NAME            print one top's machine-readable inventory record
                         (top=/define=/incdir=/derived=/src= lines) and exit
  --mode full|elaborate  full synthesis or fast hierarchy/process smoke
  --results DIRECTORY    write one machine-readable result per top/gate
  --no-structural        do not run the tied-input and tap-purity checks
  --selftest-alloc       check the YOSYS_MALLOC selection rules and exit;
                         needs neither jemalloc, yosys, sv2v nor a submodule
  -h, --help             show this help

environment:

  YOSYS_MALLOC=<path>    preload that allocator for yosys (speed only)
  YOSYS_MALLOC=none      run yosys under the system allocator
  (unset)                use jemalloc when it is installed
EOF
}

SHARD="0/1"
MODE="full"
LIST=0
EMIT=""
RESULTS=""
NO_STRUCTURAL=0
SELFTEST_ALLOC=0
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
    --emit)
      [ "$#" -ge 2 ] || { echo "--emit needs a top NAME" >&2; exit 2; }
      EMIT="$2"; shift 2 ;;
    --emit=*) EMIT="${1#--emit=}"; shift ;;
    --no-structural) NO_STRUCTURAL=1; shift ;;
    --selftest-alloc) SELFTEST_ALLOC=1; shift ;;
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
# --list deliberately derives NO sources; --emit is a source record. Answering
# both at once would have to emit the "@pp-srcs-not-derived-for---list@"
# placeholder as if it were a file.
if [ -n "$EMIT" ] && [ "$LIST" -eq 1 ]; then
  echo "--emit and --list are mutually exclusive" >&2
  exit 2
fi
# Same reason as the source guard below: --list must not pull the allocator
# rules in, so it cannot also be asked to self-test them.
if [ "$SELFTEST_ALLOC" -eq 1 ] && [ "$LIST" -eq 1 ]; then
  echo "--selftest-alloc and --list are mutually exclusive" >&2
  exit 2
fi

# The allocator rules live in one file, shared with ooc.sh. It is NOT sourced
# on the `--list` path: check_list_hermetic.sh proves --list reads nothing but
# this script and scripts/yosys_shards.py, in a tree built to hold only those
# two files (#190), so sourcing unconditionally would break that contract.
if [ "$LIST" -eq 0 ]; then
  . "$(dirname "$0")/malloc.sh"
fi

if [ "$SELFTEST_ALLOC" -eq 1 ]; then
  selftest_alloc
  exit $?
fi

export PATH="$HOME/.local/bin:$PATH"
R="$(cd "$(dirname "$0")/../.." && pwd)"
A="$R/third_party/verilog-axis/rtl"
C="$R/hdl/common"; Q="$R/hdl/ieee8021q/ts"; P="$R/hdl/ieee8021as/ptp_timestamp"
E="$R/hdl/common/eth_event_counter"; D="$R/hdl/ieee17221/adp"
F="$R/hdl/ieee8021q/filtering"
# PREPROCESSOR INPUTS AS LISTS, NOT AS ONE FLAG STRING. syn/ooc/dp_srcs.py asks
# this script for them (`--emit`) and hands them to the same front end; a flag
# string would have to be re-split by that consumer, and a consumer that re-reads
# this file rather than being handed its contents is the defect class of #235.
DEFINES=(SYNTHESIS)
INCDIRS=("$R/hdl/common" "$R/hdl/common/csr" "$Q" "$E" "$D" "$P")

# milan_datapath AND milan_csr both `include the elaboration-shape header.
# Neither has a copy beside it any more (the tracked one lives in
# hdl/common/gen/, which is already on this list), so BOTH resolve through
# this include path and a config dir prepended here overrides the shape for
# the whole design -- on every front end, not just the one that ignores the
# including file's own directory. Named once here so the flags the gate
# passes and the record `--emit` prints are the same list.
incdirs_for() {
  case "$1" in
    milan_datapath) printf '%s\n' "$R/configs/generated/endstation_arty_current" ;;
  esac
  printf '%s\n' "${INCDIRS[@]}"
}
inc_flags_for() {
  local d
  for d in "${DEFINES[@]}"; do printf -- '-D%s ' "$d"; done
  while IFS= read -r d; do printf -- '-I %s ' "$d"; done < <(incdirs_for "$1")
}
SYNTH="${YOSYS_SYNTH:-synth}"

# THE PROTOCOL PROCESSOR IS THE CONTROL PLANE (scenario B, 2026-08-13).
# The source list is derived from the checked-out submodule. Take the generator
# status explicitly: command substitution in an assignment otherwise hides a
# refusal and an empty source list can elaborate a meaningless shadow wrapper.
PP="$R/protocol-processor/hdl"
# python3 IS NEEDED ON EVERY PATH, `--list` included: the shard selector
# scripts/yosys_shards.py runs below for every invocation. Only the SOURCE
# DERIVATION under it is conditional, so this check stays unconditional -
# otherwise an absent interpreter surfaces as `Yosys shard selector fails its
# own self-test`, which reads as a repository defect rather than a missing
# runtime ([R0] on PR #191).
command -v python3 >/dev/null || {
  echo "missing tool: python3 (required by scripts/yosys_shards.py, and by" >&2
  echo "  scripts/pp_srcs.py on every path except --list)" >&2
  exit 2
}

# `--list` PRINTS NAMES AND MUST NOT NEED SOURCES. The inventory's name column
# is the first field of each `tops` row and no source path contributes to it,
# but this script used to derive the submodule source list before reaching the
# `--list` exit, so `--list` required a checked-out protocol-processor while
# saying twice above that it required nothing. That was invisible until a CI
# job called it from a checkout without submodules and `yosys-portability`
# went red in seven seconds with every shard passing (#190).
#
# The placeholder is deliberately a path that cannot exist. `--list` exits long
# before any top is built, so it is never read; if a later change moves that
# exit, sv2v (the first tool to open the sources) fails on a missing file rather
# than synthesising an empty source list, which is the failure `pp_srcs.py`
# refuses to allow in the first place.
if [ "$LIST" -eq 1 ]; then
  PP_SRCS="@pp-srcs-not-derived-for---list@"
else
  PP_DERIVED="$(python3 "$R/scripts/pp_srcs.py" --prefix "$PP")" || exit 2
  PP_SRCS="$PP_DERIVED $R/hdl/milan/KL_pp_shadow.sv $R/hdl/milan/KL_pp_maap_shim.sv"
fi

# The product-default datapath elaborates the integrated gPTP plane. Keep the
# donor package/engine list in one variable shared by its standalone wrapper
# row and the milan_datapath row; otherwise the standalone check stays green
# while hierarchy -check on the shipping default sees unresolved instances.
GPTP_ENGINE_SRCS="$R/gptp-processor/hdl/ucpu/gptp_ucpu_pkg.sv $R/gptp-processor/hdl/ucpu/KL_gptp_ucpu.sv $R/gptp-processor/hdl/wire/KL_gptp_rx_parser.sv $R/gptp-processor/hdl/wire/KL_gptp_tx_slot.sv $R/gptp-processor/hdl/common/KL_gptp_timer.sv $R/gptp-processor/hdl/top/KL_gptp_engine.sv"
GPTP_DP_SRCS="$GPTP_ENGINE_SRCS $R/hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv $R/hdl/ieee8021as/gptp_plane/KL_gptp_txstamp.sv"

# top | source files (interface modules go through their flat wrapper)
tops=(
  "tcam|$F/tcam.sv"
  "cdc_pulse|$C/cdc_pulse.sv"
  "cdc_handshake|$C/cdc_handshake.sv"
  "adp_tx_arbiter|$D/adp_tx_arbiter.sv"
  "rx_mac_filter|$F/tcam.sv $F/rx_mac_filter.sv $C/tx_ifg_gasket.sv"
  "milan_csr|$R/hdl/common/csr/milan_csr.sv"
  "KL_gptp_txstamp|$R/hdl/ieee8021as/gptp_plane/KL_gptp_txstamp.sv"
  "KL_gptp_shadow|$GPTP_ENGINE_SRCS $A/axis_fifo.v $R/hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv"
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
  "KL_media_grid_align|$R/hdl/ieee1722/crf/KL_media_grid_align.sv"
  "KL_link_guard|$C/KL_link_guard.sv"
  "KL_maap|$R/hdl/ieee1722/maap/KL_maap.sv"
  "KL_i2s_playback|$C/cdc_pair_fifo.sv $C/cdc_pulse.sv $R/hdl/ieee1722/aaf/KL_i2s_playback.sv"
  "KL_i2s_feed_mux|$R/hdl/ieee1722/aaf/KL_i2s_feed_mux.sv"
  "KL_chan_map_render|$R/hdl/ieee1722/aaf/KL_chan_map_render.sv"
  "KL_chan_map_capture|$R/hdl/ieee1722/aaf/KL_chan_map_capture.sv"
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
  "datapath_wrap|$C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $A/axis_fifo.v $A/axis_demux.v $A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v $Q/traffic_class_map.sv $Q/traffic_classifier.sv $Q/credit_based_shaper.sv $Q/traffic_shaping_core.sv $Q/traffic_queues.sv $Q/traffic_controller_802_1q.sv $R/tb/verilator/datapath/datapath_wrap.sv"
  "ptp_ts_top|$C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $A/axis_fifo.v $C/axis_mux_rr_2in_1out.sv $P/timestamp_counter.sv $P/ptp_csr_sync.sv $P/ptp_ts_core.sv $P/ptp_ts_top.sv"
  "KL_pp_shadow|$A/axis_fifo.v $PP_SRCS"
  "KL_pp_maap_shim|$R/hdl/milan/KL_pp_maap_shim.sv"
  "axis_fifo|$A/axis_fifo.v"
  "axis_demux|$A/axis_demux.v"
  "axis_arb_mux|$A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v"
  "milan_datapath|$PP_SRCS $GPTP_DP_SRCS $C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $A/axis_fifo.v $A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v $P/timestamp_counter.sv $P/ptp_csr_sync.sv $C/cdc_pulse.sv $C/cdc_handshake.sv $P/KL_ptp_clock_validity.sv $F/tcam.sv $F/rx_mac_filter.sv $C/tx_ifg_gasket.sv $R/hdl/ieee1722/aaf/KL_pcm_lpf.sv $C/KL_link_guard.sv $D/adp_tx_arbiter.sv $E/ethernet_events.sv $E/event_counter.sv $R/hdl/common/csr/milan_csr.sv $R/hdl/ieee1722/aaf/aaf_talker_i2s.sv $R/hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv $R/hdl/ieee1722/avtp/avtp_subtype_pkg.sv $R/hdl/ieee1722/avtp/avtp_stream_parser.sv $R/hdl/ieee1722/avtp/KL_stream_table.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv $R/hdl/ieee1722/crf/KL_crf_rx.sv $R/hdl/ieee1722/crf/KL_crf_tx.sv $R/hdl/ieee1722/maap/KL_maap.sv $R/hdl/ieee1722/aaf/KL_i2s_playback.sv $R/hdl/ieee1722/aaf/KL_i2s_feed_mux.sv $R/hdl/ieee1722/aaf/KL_tone_gen.sv $R/hdl/ieee1722/aaf/KL_media_adv.sv $C/cdc_pair_fifo.sv $R/hdl/ieee1722/aaf/KL_pcm_route.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv $R/hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv $R/hdl/ieee1722/aaf/KL_tdm_capture.sv $R/hdl/ieee1722/aaf/KL_aaf_packetizer.sv $R/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv $R/hdl/ieee1722/crf/KL_media_nco.sv $R/hdl/ieee1722/crf/KL_media_grid_align.sv $R/hdl/ieee1722/aaf/KL_aaf_latency_taps.sv $R/hdl/ieee1722/aaf/KL_aaf_latency_tap_bank.sv $R/hdl/ieee1722/aaf/KL_chan_map_capture.sv $R/hdl/ieee1722/aaf/KL_chan_map_render.sv $R/hdl/ieee1722/aaf/KL_tdm_render.sv $R/hdl/ieee1722/avtp/KL_media_clock_restart.sv $R/hdl/ieee1722/avtp/KL_talker_diag_ctx.sv $R/hdl/ieee1722/aaf/KL_pair_blend.sv $R/hdl/ieee1722/aaf/KL_pair_zero_fill.sv $R/hdl/ieee1722/aaf/KL_tdm_capture_master.sv $R/hdl/milan/milan_datapath.sv"
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

# `--emit NAME` HANDS ONE TOP'S RECORD TO A SECOND CONSUMER instead of letting
# it read this file. syn/ooc/dp_srcs.py, which feeds the Vivado out-of-context
# scripts, used to recognise the PP_SRCS composition and the `tops` row as text,
# and a text recogniser accepts what bash does not: a generator path this script
# would fail to execute, an argument it never passes, a commented-out row, a
# positional that is not a source ([R0] on PR #240). Everything printed below is
# bash's own expansion of the array the gate synthesises, so a mutation of this
# file either moves both consumers or fails both.
if [ -n "$EMIT" ]; then
  [ "${spec_by_name[$EMIT]+set}" = set ] || {
    echo "unknown top: $EMIT" >&2
    exit 2
  }
  emit_spec="${spec_by_name[$EMIT]}"
  printf 'top=%s\n' "$EMIT"
  for emit_d in "${DEFINES[@]}"; do printf 'define=%s\n' "$emit_d"; done
  while IFS= read -r emit_d; do printf 'incdir=%s\n' "$emit_d"; done \
    < <(incdirs_for "$EMIT")
  # The generated half, named so the consumer can assert it survived whole.
  for emit_f in ${PP_DERIVED:-}; do printf 'derived=%s\n' "$emit_f"; done
  # UNQUOTED on purpose: this is the same word splitting that builds sv2v's
  # argument list below, so the record cannot hold a token the gate would not.
  for emit_f in ${emit_spec#*|}; do printf 'src=%s\n' "$emit_f"; done
  exit 0
fi

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

# Resolved once, after the tool check, so a machine missing yosys is told that
# and not something about an allocator.
MALLOC_LIB="$(select_malloc)" || exit 2

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

# Relative $readmemh images must exist in Yosys's working directory, so they
# are generated into $TMP and Yosys runs from there. They used to be written
# into the CALLER's directory, which for the documented invocation (this script
# run from the repository root: CONTRIBUTING 2.1, both CI workers) is the root
# of the checkout, where nothing ignores them; only `syn/yosys/*.hex` is, which
# covers the `make` flow and no other. Three such images rode into a commit of
# PR #191 exactly that way, byte-identical to what this block generates.
for generator in \
  "$R/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py" \
  "$R/protocol-processor/hdl/aecp/ucode/gen_ucode.py" \
  "$R/gptp-processor/hdl/ucode/gen_gptp_ucode.py"; do
  [ -f "$generator" ] || {
    echo "Yosys: required ROM generator is missing: $generator" >&2
    exit 2
  }
done
python3 "$R/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py" -o "$TMP/ltn_rom.hex" >/dev/null || {
  echo "Yosys: ACMP transition-ROM generation failed" >&2; exit 2;
}
python3 "$R/protocol-processor/hdl/aecp/ucode/gen_ucode.py" -o "$TMP/ucode.hex" >/dev/null || {
  echo "Yosys: AECP microcode generation failed" >&2; exit 2;
}
python3 "$R/gptp-processor/hdl/ucode/gen_gptp_ucode.py" -o "$TMP/gptp_ucode.hex" >/dev/null || {
  echo "Yosys: gPTP microcode generation failed" >&2; exit 2;
}
for image in "$TMP/ltn_rom.hex" "$TMP/ucode.hex" "$TMP/gptp_ucode.hex"; do
  [ -s "$image" ] || { echo "Yosys: generated ROM is empty: $image" >&2; exit 2; }
done

if [ "$MODE" = full ]; then
  echo "== Yosys open-synthesis check ($SYNTH, via sv2v; shard $shard_index/$shard_total) =="
else
  echo "== Yosys fast elaboration check (via sv2v) =="
fi
# Named, because a wall-clock figure quoted from this output is only
# reproducible if the allocator that produced it is on the record (#286).
echo "   yosys allocator: ${MALLOC_LIB:-system}"
pass=0
fail=0
for name in "${selected_names[@]}"; do
  spec="${spec_by_name[$name]}"
  top="${spec%%|*}"
  srcs="${spec#*|}"
  inc="$(inc_flags_for "$top")"

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
  # The recorded cell count comes from `stat -json`, never from the human
  # table. The text total changed spelling between Yosys releases (0.33's
  # `Number of cells:` against 0.66's `NNN cells`) and its `=== design
  # hierarchy ===` section is not printed at all for a top with no
  # submodules, which is how every CI record and 29 of 46 local records came
  # to read `cells=?` (#287). `design.num_cells` in the JSON is the same
  # hierarchy-rollup total the text section prints and it exists in both the
  # hierarchical and the single-module case; when it is missing the top FAILS
  # below instead of publishing a placeholder that looks like evidence.
  program="$program; tee -q -o $TMP/$top.stat.json stat -top $top -json"
  # The preload is exported INSIDE the subshell, so it reaches yosys and the
  # children yosys spawns - `abc`, which is 16% of the heaviest top - and dies
  # with them. sv2v above is a GHC binary and the helpers are python3, and
  # neither was measured under a replacement allocator. Proved rather than
  # asserted: preloading a library that records `program_invocation_short_name`
  # over one top logs yosys, sh and abc, and neither sv2v nor python3.
  (
    cd "$TMP" || exit 2
    apply_malloc_env "$MALLOC_LIB"
    yosys -p "$program"
  ) > "$TMP/$top.yos.log" 2>&1
  rc=$?
  cells="$(python3 - "$TMP/$top.stat.json" <<'PY'
import json
import sys

try:
    with open(sys.argv[1], encoding="utf-8") as handle:
        value = json.load(handle)["design"]["num_cells"]
except (OSError, ValueError, KeyError):
    raise SystemExit(0)
if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
    print(value)
PY
)"
  if [ "$rc" -eq 0 ] && [ -n "$cells" ]; then
    printf "  [PASS] %-22s cells=%s\n" "$top" "$cells"
    record_result top "$top" PASS 1 "$MODE" "$cells"
    pass=$((pass + 1))
  elif [ "$rc" -eq 0 ]; then
    # yosys exited 0 but produced no measurable total: FAIL, never `cells=?`.
    # The published record is the gate's evidence, and scripts/yosys_tally.py
    # refuses a PASS record without a numeric count for the same reason.
    printf "  [FAIL] %-22s stat: no design cell count in %s.stat.json\n" "$top" "$top"
    record_result top "$top" FAIL 1 "$MODE" ""
    fail=$((fail + 1))
  else
    # yosys 0.66 (the version a bench box may run) prints a $readmemh failure as
    # `<file>:<line>: ERROR: ...`, so an anchored `^ERROR` matches nothing and the
    # reason column comes out EMPTY - indistinguishable from an OOM-killed tool
    # (#192). Match ERROR wherever it sits and drop the path:line prefix.
    reason="$(grep -oE 'ERROR:.*' "$TMP/$top.yos.log" | head -1)"
    printf "  [FAIL] %-22s yosys: %s\n" "$top" "$reason"
    record_result top "$top" FAIL 1 "$MODE" ""
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
