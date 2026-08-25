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
#   ./ooc.sh --record-rom-digests  # re-record rom_digests.tsv at the pin
#                                  # (a pin-bump step; the diff is reviewed)
#
# Exit status is the gate (#245): non-zero if any requested top fails sv2v or
# yosys, if a ROM generator fails or emits an empty or WRONG-SHAPED image
# (word count and width are validated against the pinned packages) or a
# wrong-CONTENT image (sha256 against rom_digests.tsv, keyed by the
# protocol-processor pin), if staging or publication fails, if the report
# phase fails (no stat block for the top, a block mapping to zero xc7
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
#   - the geometry PACKAGES are found IN the derived population above, never
#     spelled as paths here ([R0] round two: a spelled path is a hand list
#     in waiting, and the literal gate cannot see shell semantics);
#   - the expected geometry comes from the ONE live declaration in each
#     package, comments stripped first and the name boundary-anchored: a
#     stale value in a comment must never win, and zero, duplicate or
#     unsupported (expression) spellings refuse rather than guess;
#   - after //-comment stripping the image must hold EXACTLY depth words of
#     EXACTLY width/4 hex digits (x/z refused: a word that loads X is priced
#     as X);
#   - the image CONTENT must match the sha256 recorded for this
#     protocol-processor pin in rom_digests.tsv: a correctly SHAPED wrong
#     image (a regressed generator emitting all-zero words) passed every
#     shape gate and priced KL_pp_shadow 4,045 LUT_TOT low ([R0] round two).
#     A pin bump re-records with --record-rom-digests, and that diff is
#     reviewed with the bump;
#   - each image is generated into an EXCLUSIVELY created staging file
#     (mktemp, never a predictable name a stale file could squat) and
#     published by a checked rename only after it validates; the published
#     target must be a regular file. OOC_TMP is reusable across runs.
one_pp_source() { # <basename> -> the ONE population entry carrying it, or die
  local hits n
  hits=$(printf '%s\n' $PP_DERIVED | grep "/$1\$")
  n=$(printf '%s\n' "$hits" | grep -c .)
  if [ "$n" -ne 1 ]; then
    echo "ooc.sh: FATAL: expected exactly one $1 in the derived processor population, found $n - geometry comes from the record pp_srcs.py hands this script, and it did not" >&2
    exit 2
  fi
  printf '%s' "$hits"
}
pkg_num() { # <file> <name> -> the ONE live declaration's decimal value, or die
  python3 - "$1" "$2" <<'PKG_EOF'
import re, sys
path, name = sys.argv[1], sys.argv[2]
text = open(path).read()
text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
text = re.sub(r"//.*", "", text)
pat = re.compile(r"^\s*(?:localparam|parameter)\b[^=;]*?\b%s\b\s*=\s*(\d+)\s*;"
                 % re.escape(name), re.M)
hits = pat.findall(text)
if len(hits) != 1:
    sys.stderr.write("ooc.sh: FATAL: expected exactly one live declaration "
                     "of %s in %s, found %d (comments stripped; an "
                     "unsupported spelling is a refusal, not a guess)\n"
                     % (name, path, len(hits)))
    sys.exit(1)
print(hits[0])
PKG_EOF
}
# A declared ROM width must be a positive multiple of 4, and a depth must
# be positive. The image contract is EXACT hex digits per word; truncating
# a 50-bit declaration to 50/4 = 12 digits would let a stale 48-bit image
# satisfy it with the new high bits silently zero-filled ([R-parallel]
# round three on PR #264 probed exactly that in the sibling Vivado recipe,
# and this script shared the arithmetic). No pinned ROM is
# non-nibble-aligned; if one ever becomes so, THIS refusal is where ceiling
# division plus a high-bits-zero check must be added - never a guess.
nibble_width() { # <name> <value> -> value, or die
  case "$2" in
    ''|*[!0-9]*) : ;;
    *) if [ "$2" -gt 0 ] && [ $(( $2 % 4 )) -eq 0 ]; then printf '%s' "$2"; return 0; fi ;;
  esac
  echo "ooc.sh: FATAL: $1 = $2 is not a positive nibble-aligned ROM width - a truncated digit count would accept a stale undersized image; add ceiling division AND a high-bits-zero check before accepting such a width" >&2
  exit 2
}
positive_depth() { # <name> <value> -> value, or die
  case "$2" in
    ''|*[!0-9]*) : ;;
    *) if [ "$2" -gt 0 ]; then printf '%s' "$2"; return 0; fi ;;
  esac
  echo "ooc.sh: FATAL: $1 = $2 is not a positive ROM depth (an expected word count of zero would let an empty image validate)" >&2
  exit 2
}
UCPU_PKG=$(one_pp_source ucpu_pkg.sv)     || exit 2
ACMP_PKG=$(one_pp_source pp_acmp_pkg.sv)  || exit 2
UCODE_W=$(pkg_num "$UCPU_PKG" UCODE_W_C)  || exit 2
UCODE_W=$(nibble_width UCODE_W_C "$UCODE_W") || exit 2
UPC_W=$(pkg_num "$UCPU_PKG" UPC_W_C)      || exit 2
TROM_W=$(pkg_num "$ACMP_PKG" TROM_W_C)    || exit 2
TROM_W=$(nibble_width TROM_W_C "$TROM_W") || exit 2
TROM_D=$(pkg_num "$ACMP_PKG" TROM_DEPTH_C) || exit 2
TROM_D=$(positive_depth TROM_DEPTH_C "$TROM_D") || exit 2

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

# The content ledger: sha256 per (protocol-processor pin, image), tracked.
DIGESTS="$R/syn/yosys/rom_digests.tsv"
PP_PIN=$(git -C "$R/protocol-processor" rev-parse HEAD) || {
  echo "ooc.sh: FATAL: cannot read the protocol-processor checkout revision" >&2
  exit 2
}
RECORD=0
if [ "${1:-}" = "--record-rom-digests" ]; then RECORD=1; shift; fi

new_rows=""
for rom_spec in \
    "ltn_rom.hex|$R/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py|$TROM_W|$TROM_D" \
    "ucode.hex|$R/protocol-processor/hdl/aecp/ucode/gen_ucode.py|$UCODE_W|$((1 << UPC_W))"; do
  IFS='|' read -r img gen width depth <<< "$rom_spec"
  digits=$((width / 4))
  if ! rm -f "$TMP/$img"; then
    echo "ooc.sh: FATAL: cannot remove the previous $img in $TMP (a directory or unwritable entry is squatting the target)" >&2
    exit 2
  fi
  if ! stage=$(mktemp "$TMP/$img.stage.XXXXXXXX"); then
    echo "ooc.sh: FATAL: cannot create an exclusive staging file for $img in $TMP" >&2
    exit 2
  fi
  if ! python3 "$gen" -o "$stage" >/dev/null; then
    rm -f "$stage"
    echo "ooc.sh: FATAL: ROM generator failed: $gen ($img is a \$readmemh input of the control plane)" >&2
    exit 2
  fi
  if ! diag=$(rom_check "$stage" "$digits" "$depth"); then
    rm -f "$stage"
    echo "ooc.sh: FATAL: $img is malformed after generation by $gen: ${diag:-empty image} (expected ${depth}x${width}-bit) - refusing to measure a ROM \$readmemh would part-fill with X" >&2
    exit 2
  fi
  got=$(sha256sum < "$stage" | awk '{print $1}')
  if [ "$RECORD" -eq 1 ]; then
    new_rows="${new_rows}${PP_PIN}	${img}	${got}
"
  else
    want=$(awk -v p="$PP_PIN" -v i="$img" '$1 == p && $2 == i { print $3 }' "$DIGESTS" 2>/dev/null | head -1)
    if [ -z "$want" ]; then
      rm -f "$stage"
      echo "ooc.sh: FATAL: no recorded content digest for $img at protocol-processor pin $PP_PIN in syn/yosys/rom_digests.tsv - a pin bump re-records with ./ooc.sh --record-rom-digests, and that diff is reviewed with the bump" >&2
      exit 2
    fi
    if [ "$got" != "$want" ]; then
      rm -f "$stage"
      echo "ooc.sh: FATAL: content digest mismatch for $img at pin $PP_PIN: generated $got, recorded $want - the generator regressed (a correctly shaped wrong image still prices wrong) or the ledger is stale" >&2
      exit 2
    fi
  fi
  if ! mv "$stage" "$TMP/$img"; then
    rm -f "$stage"
    echo "ooc.sh: FATAL: cannot publish $img into $TMP" >&2
    exit 2
  fi
  if [ ! -f "$TMP/$img" ] || [ -L "$TMP/$img" ]; then
    echo "ooc.sh: FATAL: published $img in $TMP is not a regular file" >&2
    exit 2
  fi
done

if [ "$RECORD" -eq 1 ]; then
  # Rewrite this pin's rows, keep every other pin's, keep the header.
  if ! { grep -h '^#' "$DIGESTS" 2>/dev/null
         { grep -hv '^#' "$DIGESTS" 2>/dev/null | awk -v p="$PP_PIN" '$1 != p'
           printf '%s' "$new_rows"; } | sort; } > "$DIGESTS.new.$$"; then
    rm -f "$DIGESTS.new.$$"
    echo "ooc.sh: FATAL: cannot rewrite syn/yosys/rom_digests.tsv" >&2
    exit 2
  fi
  mv "$DIGESTS.new.$$" "$DIGESTS" || exit 2
  echo "ooc.sh: recorded ROM content digests for protocol-processor pin $PP_PIN in syn/yosys/rom_digests.tsv"
  exit 0
fi

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
    printf "%-28s report FAIL: yosys left no (or an empty) JSON netlist artifact (%s)\n" "$top" "$TMP/$top.ooc.json"; status=1; continue
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
