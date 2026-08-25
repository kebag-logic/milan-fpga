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
# Exit status is the gate (#245): non-zero if any requested top fails sv2v or
# yosys, if a ROM generator fails or emits an empty or WRONG-SHAPED image
# (word count and width are validated against the pinned packages), if the
# report phase fails (no stat block for the top, a block mapping to zero xc7
# cells, a dead awk, or a missing/empty JSON artifact), or if a requested
# top is not in the list. A failed top used to print its error and leave the
# script exiting 0, which read as "the whole list passed" to any caller.
#
# Requires: yosys, sv2v (see README.md).
# Self-test: syn/yosys/ooc_selftest.py drives the refusals on planted failures.

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

# ...and with the processor come its ROMs. protocol_processor_top $readmemh's
# the ACMP listener transition image by the RELATIVE name "ltn_rom.hex", and
# KL_aecp_ucpu its microcode by "ucode.hex" (UCODE_HEX_P) -- yosys resolves
# both against ITS OWN working directory, not against the source file.
# Generate BOTH into $TMP and run yosys FROM $TMP (below), so a run from the
# repository root leaves nothing behind - the same fix syn/yosys/run.sh carries
# (#191): only syn/yosys/*.hex is gitignored, so a stray image in the
# caller's directory is one broad `git add` from being committed (#192).
#
# Generation is FATAL on failure, and a wrong-SHAPED image is a failure like
# an absent one (#245, and its [R-parallel] round: a one-word ucode.hex is
# "non-empty", loads, leaves 2,047 words X, and produced a plausible row
# 4,045 LUT_TOT under the true figure). $readmemh does not police geometry,
# so this script does, BEFORE a number can exist:
#   - the expected geometry is DERIVED from the pinned packages
#     (ucpu_pkg.sv: UCODE_W_C x 2^UPC_W_C; pp_acmp_pkg.sv: TROM_W_C x
#     TROM_DEPTH_C), never copied here where it would drift;
#   - after //-comment stripping the image must hold EXACTLY depth words of
#     EXACTLY width/4 hex digits (x/z refused: a word that loads X is priced
#     as X);
#   - each image is generated into a fresh temp target and published by
#     rename only after it validates, so a stale or half-written file can
#     never be the one yosys reads (OOC_TMP is reusable across runs).
pkg_num() { # <file> <localparam name> -> its decimal value, or die
  local v
  v=$(sed -n "s/.*$2 *= *\([0-9][0-9]*\).*/\1/p" "$1" | head -1)
  if [ -z "$v" ]; then
    echo "ooc.sh: FATAL: cannot derive $2 from $1 (geometry source moved?)" >&2
    exit 2
  fi
  printf '%s' "$v"
}
UCODE_W=$(pkg_num "$PP/aecp/ucpu_pkg.sv" UCODE_W_C)      || exit 2
UPC_W=$(pkg_num "$PP/aecp/ucpu_pkg.sv" UPC_W_C)          || exit 2
TROM_W=$(pkg_num "$PP/acmp/pp_acmp_pkg.sv" TROM_W_C)     || exit 2
TROM_D=$(pkg_num "$PP/acmp/pp_acmp_pkg.sv" TROM_DEPTH_C) || exit 2

rom_check() { # <file> <hex digits per word> <word count> ; diagnostics on stdout
  awk -v digits="$2" -v words="$3" '
    { sub(/\/\/.*$/, "")
      for (i = 1; i <= NF; i++) {
        n++
        if ($i !~ /^[0-9a-fA-F]+$/ || length($i) != digits) {
          printf "word %d (%s) is not exactly %d hex digits\n", n, $i, digits
          exit 1
        }
      }
    }
    END { if (n != words) { printf "%d words, expected exactly %d\n", n, words; exit 1 } }
  ' "$1"
}

for rom_spec in \
    "ltn_rom.hex|$R/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py|$TROM_W|$TROM_D" \
    "ucode.hex|$R/protocol-processor/hdl/aecp/ucode/gen_ucode.py|$UCODE_W|$((1 << UPC_W))"; do
  IFS='|' read -r img gen width depth <<< "$rom_spec"
  digits=$((width / 4))
  rm -f "$TMP/$img"
  if ! python3 "$gen" -o "$TMP/$img.gen.$$" >/dev/null; then
    rm -f "$TMP/$img.gen.$$"
    echo "ooc.sh: FATAL: ROM generator failed: $gen ($img is a \$readmemh input of the control plane)" >&2
    exit 2
  fi
  if ! diag=$(rom_check "$TMP/$img.gen.$$" "$digits" "$depth"); then
    rm -f "$TMP/$img.gen.$$"
    echo "ooc.sh: FATAL: $img is malformed after generation by $gen: ${diag:-empty image} (expected ${depth}x${width}-bit) - refusing to measure a ROM \$readmemh would part-fill with X" >&2
    exit 2
  fi
  mv "$TMP/$img.gen.$$" "$TMP/$img"
done

DP_SRCS="$PP_SRCS $C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $A/axis_fifo.v $A/axis_demux.v $A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v $Q/traffic_class_map.sv $Q/traffic_classifier.sv $Q/credit_based_shaper.sv $Q/traffic_shaping_core.sv $Q/traffic_queues.sv $Q/traffic_controller_802_1q.sv $P/timestamp_counter.sv $P/ptp_csr_sync.sv $C/cdc_pulse.sv $C/cdc_handshake.sv $C/axis_mux_rr_2in_1out.sv $P/ptp_ts_core.sv $P/ptp_ts_top.sv $F/tcam.sv $F/rx_mac_filter.sv $C/tx_ifg_gasket.sv $R/hdl/ieee1722/aaf/KL_pcm_lpf.sv $C/KL_link_guard.sv $D/adp_tx_arbiter.sv $E/ethernet_events.sv $E/event_counter.sv $R/hdl/common/csr/milan_csr.sv $R/hdl/ieee1722/aaf/aaf_talker_i2s.sv $R/hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv $R/hdl/ieee1722/avtp/avtp_subtype_pkg.sv $R/hdl/ieee1722/avtp/avtp_stream_parser.sv $R/hdl/ieee1722/avtp/KL_stream_table.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv $R/hdl/ieee1722/crf/KL_crf_rx.sv $R/hdl/ieee1722/crf/KL_crf_tx.sv $R/hdl/ieee1722/maap/KL_maap.sv $R/hdl/ieee1722/aaf/KL_i2s_playback.sv $R/hdl/ieee1722/aaf/KL_i2s_feed_mux.sv $R/hdl/ieee1722/aaf/KL_tone_gen.sv $R/hdl/ieee1722/aaf/KL_media_adv.sv $C/cdc_pair_fifo.sv $R/hdl/ieee1722/aaf/KL_pcm_route.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv $R/hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv $R/hdl/ieee1722/aaf/KL_tdm_capture.sv $R/hdl/ieee1722/aaf/KL_aaf_packetizer.sv $R/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv $R/hdl/ieee1722/crf/KL_media_nco.sv $R/hdl/ieee1722/aaf/KL_aaf_latency_taps.sv $R/hdl/ieee1722/aaf/KL_chan_map_capture.sv $R/hdl/ieee1722/aaf/KL_chan_map_render.sv $R/hdl/ieee1722/aaf/KL_pcm_tx.sv $R/hdl/ieee1722/aaf/KL_tdm_render.sv $R/hdl/milan/milan_datapath.sv $R/hdl/ieee1722/aaf/KL_tdm_capture_master.sv $R/hdl/ieee1722/aaf/KL_pair_blend.sv $R/hdl/ieee1722/aaf/KL_pair_zero_fill.sv $R/hdl/ieee1722/avtp/KL_talker_diag_ctx.sv $R/hdl/ieee1722/avtp/KL_media_clock_restart.sv $R/hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv"

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
  # The saved-state backing store's BEFORE/AFTER pair
  # (docs/design/SAVED_STATE_FASTCONNECT.md section 8.3). These are
  # sizing sketches under syn/ooc/sizing/, NOT shipping RTL: nothing
  # instantiates them and hdl/ never sees them. They are here so the
  # decision record can quote a measured bound for the backend that
  # replaces KL_pp_shadow's blank-flash responder, at both shapes,
  # through OOC_CHPARAM.
  "KL_nvm_blankflash_sizer|$R/syn/ooc/sizing/KL_nvm_blankflash_sizer.sv"
  "KL_nvm_backend_sizer|$R/syn/ooc/sizing/KL_nvm_backend_sizer.sv"
)

want=("$@")
# A requested name that matches no list entry must refuse, not print a bare
# header and exit 0 (#245): the silent no-op is the same false green as a
# swallowed synth failure, and a typo is exactly how it happens.
for w in "${want[@]}"; do
  known=0
  for spec in "${tops[@]}"; do [ "${spec%%|*}" = "$w" ] && known=1; done
  if [ "$known" -eq 0 ]; then
    echo "ooc.sh: FATAL: unknown top '$w' - not in this script's tops list" >&2
    exit 2
  fi
done
status=0
printf "== OOC area (synth_xilinx -family xc7 -flatten) ==\n"
printf "%-28s %8s %8s %8s %8s %8s %8s %8s %8s\n" \
       top LUT LUTRAM LUT_TOT FF RAMB36 RAMB18 DSP CARRY4
for spec in "${tops[@]}"; do
  top="${spec%%|*}"; srcs="${spec#*|}"
  if [ ${#want[@]} -gt 0 ]; then
    hit=0; for w in "${want[@]}"; do [ "$w" = "$top" ] && hit=1; done
    [ $hit -eq 1 ] || continue
  fi
  if ! sv2v --top="$top" $INC $srcs > "$TMP/$top.ooc.v" 2> "$TMP/$top.ooc.sv2v.err"; then
    printf "%-28s sv2v FAIL: %s\n" "$top" "$(head -1 "$TMP/$top.ooc.sv2v.err")"; status=1; continue
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
  # OOC_NODSP=1 maps constant multipliers to LUT+CARRY4 instead of DSP48E1.
  # Both mappings are legal, and a block whose only DSPs come from constant
  # strides is priced honestly only if BOTH are published: the DSP column
  # hides LUTs, and the LUT-only column is the worst case.
  nodsp=""; [ -n "${OOC_NODSP:-}" ] && nodsp=" -nodsp"
  rm -f "$TMP/$top.ooc.json"
  (cd "$TMP" && yosys -p "read_verilog $TMP/$top.ooc.v;$chp synth_xilinx -family xc7$nodsp -top $top -flatten; stat; write_json $TMP/$top.ooc.json") \
    > "$TMP/$top.ooc.log" 2>&1
  if [ $? -ne 0 ]; then
    printf "%-28s yosys FAIL: %s\n" "$top" "$(grep -oE 'ERROR:.*' "$TMP/$top.ooc.log" | head -1)"; status=1; continue
  fi
  # yosys said 0; the REPORT phase must fail closed too ([R-parallel] on
  # #245): the JSON artifact the command names must exist non-empty (its
  # absence means the netlist was never written, whatever the log says), and
  # the row must come from a real parsed stat block, never be manufactured by
  # an END clause over an empty parse.
  if ! [ -s "$TMP/$top.ooc.json" ]; then
    printf "%-28s report FAIL: yosys left no JSON netlist artifact (%s)\n" "$top" "$TMP/$top.ooc.json"; status=1; continue
  fi
  # count from the final (post-flatten) `stat` block only. yosys prints
  # "<count>   <CELLTYPE>", so the count is $1 and the type is $2.
  #
  # THE LUTRAM COLUMN IS NOT DECORATION. It was added because its absence made
  # this script UNDER-COUNT, and by enough to matter: the saved-state backend
  # candidate mapped its two 8-entry channel-map tables to 32 RAM32M cells at
  # the 8x8 shape, and the old awk counted only LUT[1-6], so 128 LUT6 of
  # SLICEM sat in no column at all and the block read 128 LUT cheaper than it
  # is. A distributed-RAM mapping is legal and is usually the cheap one; what
  # is not legal is pricing a block as though those LUTs were free.
  #
  # LUT_TOT is LUT plus the LUT6 equivalents of the distributed RAM, from
  # UG474 (7 Series CLB): RAM32M and RAM64M and RAM128X1D and RAM256X1S each
  # occupy 4 LUT6 of a SLICEM; RAM32X1D, RAM64X1D and RAM128X1S occupy 2;
  # RAM32X1S and RAM64X1S occupy 1.
  #
  # A pristine log carries TWO top-named blocks (synth_xilinx prints its own
  # final statistics, then the explicit `stat` prints again); both are
  # post-mapping, and the LAST one wins deterministically. The parse REFUSES
  # (nonzero awk exit, diagnostic on stdout) when no block was seen, and when
  # the winning block maps to zero xc7 cells - an all-zero row is what an
  # unmapped or absent design prints, never a measurement. The awk's own exit
  # status is taken: a parse that dies is a failed top, not a missing row.
  if row=$(awk -v top="$top" '
    function lram_luts(t) {
      if (t == "RAM32M" || t == "RAM64M" || t == "RAM128X1D" ||
          t == "RAM32M16" || t == "RAM64M8" || t == "RAM256X1S") return 4;
      if (t == "RAM32X1D" || t == "RAM64X1D" || t == "RAM128X1S") return 2;
      if (t == "RAM32X1S" || t == "RAM64X1S") return 1;
      return 0;
    }
    /^=== .* ===$/ { inblk = 0 }
    $0 == "=== " top " ===" { blocks++; inblk=1; lut=0; lrm=0; ff=0; r36=0; r18=0; dsp=0; c4=0 }
    inblk && $2 ~ /^LUT[1-6]$/     { lut += $1 }
    inblk && $2 ~ /^RAM[0-9]/      { lrm += $1 * lram_luts($2) }
    inblk && $2 ~ /^FD[CPRS]E?$/   { ff  += $1 }
    inblk && $2 ~ /^RAMB36E1$/     { r36 += $1 }
    inblk && $2 ~ /^RAMB18E1$/     { r18 += $1 }
    inblk && $2 ~ /^DSP48E1$/      { dsp += $1 }
    inblk && $2 ~ /^CARRY4$/       { c4  += $1 }
    END {
      if (blocks == 0) { printf "no stat block for %s in the log", top; exit 3 }
      if (lut + lrm + ff + r36 + r18 + dsp + c4 == 0) {
        printf "final stat block for %s maps to zero xc7 cells (unmapped or empty design)", top; exit 4
      }
      printf "%-28s %8d %8d %8d %8d %8d %8d %8d %8d", \
             top, lut, lrm, lut + lrm, ff, r36, r18, dsp, c4
    }
  ' "$TMP/$top.ooc.log"); then
    printf '%s\n' "$row"
  else
    printf "%-28s report FAIL: %s\n" "$top" "${row:-stat parse died}"; status=1; continue
  fi
done
[ -n "${OOC_TMP:-}" ] || rm -rf "$TMP"
# The cleanup above must not launder a failed top back into success: exit with
# the accumulated verdict, not with the last statement's (#245).
exit "$status"
