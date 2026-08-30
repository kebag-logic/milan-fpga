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
# wrong-CONTENT image (sha256 against rom_digests.tsv, keyed by the owning
# processor's superproject pin), if staging or publication fails, if a published
# image is gone or hashes differently at ANY consumption (each top's yosys
# run consumes an exclusive read-only copy, re-hashed before and after the
# run - a swap or delete after publication, or between two tops, must never
# price), if the report phase fails (no stat block for the top, a block
# mapping to zero xc7 cells, a dead awk, or a missing/empty JSON artifact),
# or if a requested top is not in the list. A failed top used to print its
# error and leave the script exiting 0, which read as "the whole list
# passed" to any caller.
#
# Requires: yosys, sv2v (see README.md).
# Self-test: syn/yosys/ooc_selftest.py drives the refusals on planted failures.

set -u
# The allocator rules, shared with run.sh. This script never moves the main
# shell's directory - every yosys run happens in a `(cd "$rundir" && ...)`
# subshell - so a relative YOSYS_MALLOC resolves against the caller's directory
# as they meant it, and the selection below can sit anywhere before the runs.
. "$(dirname "$0")/malloc.sh"
if [ "${1:-}" = "--selftest-alloc" ]; then selftest_alloc; exit $?; fi
export PATH="$HOME/.local/bin:$PATH"
R="$(cd "$(dirname "$0")/../.." && pwd)"
A="$R/third_party/verilog-axis/rtl"
C="$R/hdl/common"; Q="$R/hdl/ieee8021q/ts"; P="$R/hdl/ieee8021as/ptp_timestamp"
E="$R/hdl/common/eth_event_counter"; D="$R/hdl/ieee17221/adp"
F="$R/hdl/ieee8021q/filtering"
INC="-DSYNTHESIS -I $R/hdl/common -I $R/hdl/common/csr -I $Q -I $E -I $D -I $P"
TMP="${OOC_TMP:-$(mktemp -d)}"; mkdir -p "$TMP"
# An OOC_TMP the caller spelled RELATIVELY is resolved once, here. yosys runs
# from a per-top run directory below, so it would resolve a relative $TMP
# against THAT directory and every top would fail with "File `relt/x.ooc.v'
# not found" - a path nobody typed, naming neither the knob nor the cause.
TMP="$(cd "$TMP" && pwd -P)" || exit 2
# ONE cleanup, not one per refusal. This gate has ~30 fatal exits and each of
# them used to leak the mktemp'd tree (both ROM images at the earliest
# refusal, plus a 10 MB JSON once a top has been written), on a box with a
# per-user tmpfs quota. Worse, a run directory this script LOCKS (chmod u-w,
# below) is not removable by a later `rm -rf` at all until it is unlocked, so
# an interrupt between the lock and the unlock stranded a directory the
# operator had to chmod by hand. syn/yosys/run.sh:296 already carries the
# same trap. OOC_TMP still means "keep the artefacts".
RUNDIR=""
ooc_cleanup() {
  [ -z "$RUNDIR" ] || { chmod u+w "$RUNDIR" 2>/dev/null; rm -rf "$RUNDIR"; }
  [ -z "${LEDGER_STAGE:-}" ] || rm -f "$LEDGER_STAGE"
  [ -n "${OOC_TMP:-}" ] || rm -rf "$TMP"
}
trap ooc_cleanup EXIT

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
GPTP_ENGINE_SRCS="$R/gptp-processor/hdl/ucpu/gptp_ucpu_pkg.sv $R/gptp-processor/hdl/ucpu/KL_gptp_ucpu.sv $R/gptp-processor/hdl/wire/KL_gptp_rx_parser.sv $R/gptp-processor/hdl/wire/KL_gptp_tx_slot.sv $R/gptp-processor/hdl/common/KL_gptp_timer.sv $R/gptp-processor/hdl/top/KL_gptp_engine.sv"
GPTP_DP_SRCS="$GPTP_ENGINE_SRCS $R/hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv $R/hdl/ieee8021as/gptp_plane/KL_gptp_txstamp.sv"

# THE ARGUMENTS ARE VALIDATED FIRST. Everything below this block - the pin
# read, the geometry parse, both ROM generations, the digest ledger - is
# expensive, needs an initialised submodule, and can refuse; running it
# before the requested names are checked meant `./ooc.sh KL_chan_map_rendr`
# generated and published both ROMs and then, on a freshly bumped pin,
# refused with "no recorded content digest" for a top that does not exist.
# The tops list needs nothing but the path variables and $PP_SRCS.
DP_SRCS="$PP_SRCS $GPTP_DP_SRCS $C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $A/axis_fifo.v $A/axis_demux.v $A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v $Q/traffic_class_map.sv $Q/traffic_classifier.sv $Q/credit_based_shaper.sv $Q/traffic_shaping_core.sv $Q/traffic_queues.sv $Q/traffic_controller_802_1q.sv $P/timestamp_counter.sv $P/ptp_csr_sync.sv $C/cdc_pulse.sv $C/cdc_handshake.sv $C/axis_mux_rr_2in_1out.sv $P/ptp_ts_core.sv $P/ptp_ts_top.sv $F/tcam.sv $F/rx_mac_filter.sv $C/tx_ifg_gasket.sv $R/hdl/ieee1722/aaf/KL_pcm_lpf.sv $C/KL_link_guard.sv $D/adp_tx_arbiter.sv $E/ethernet_events.sv $E/event_counter.sv $R/hdl/common/csr/milan_csr.sv $R/hdl/ieee1722/aaf/aaf_talker_i2s.sv $R/hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv $R/hdl/ieee1722/avtp/avtp_subtype_pkg.sv $R/hdl/ieee1722/avtp/avtp_stream_parser.sv $R/hdl/ieee1722/avtp/KL_stream_table.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv $R/hdl/ieee1722/crf/KL_crf_rx.sv $R/hdl/ieee1722/crf/KL_crf_tx.sv $R/hdl/ieee1722/maap/KL_maap.sv $R/hdl/ieee1722/aaf/KL_i2s_playback.sv $R/hdl/ieee1722/aaf/KL_i2s_feed_mux.sv $R/hdl/ieee1722/aaf/KL_tone_gen.sv $R/hdl/ieee1722/aaf/KL_media_adv.sv $C/cdc_pair_fifo.sv $R/hdl/ieee1722/aaf/KL_pcm_route.sv $R/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv $R/hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv $R/hdl/ieee1722/aaf/KL_tdm_capture.sv $R/hdl/ieee1722/aaf/KL_aaf_packetizer.sv $R/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv $R/hdl/ieee1722/crf/KL_media_nco.sv $R/hdl/ieee1722/aaf/KL_aaf_latency_taps.sv $R/hdl/ieee1722/aaf/KL_aaf_latency_tap_bank.sv $R/hdl/ieee1722/aaf/KL_chan_map_capture.sv $R/hdl/ieee1722/aaf/KL_chan_map_render.sv $R/hdl/ieee1722/aaf/KL_pcm_tx.sv $R/hdl/ieee1722/aaf/KL_tdm_render.sv $R/hdl/milan/milan_datapath.sv $R/hdl/ieee1722/aaf/KL_tdm_capture_master.sv $R/hdl/ieee1722/aaf/KL_pair_blend.sv $R/hdl/ieee1722/aaf/KL_pair_zero_fill.sv $R/hdl/ieee1722/avtp/KL_talker_diag_ctx.sv $R/hdl/ieee1722/avtp/KL_media_clock_restart.sv $R/hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv"

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

# Print bash's own expansion of DP_SRCS and exit. scripts/check_rtl_source_lists.py
# grades what this script will really read, not a model of this file: a
# recogniser accepts what it has modelled and bash accepts something else
# (syn/ooc/dp_srcs.py records four escapes that worked exactly that way).
if [ "${1:-}" = "--emit-dp" ]; then
  printf '%s\n' $DP_SRCS
  exit 0
fi

RECORD=0
if [ "${1:-}" = "--record-rom-digests" ]; then RECORD=1; shift; fi
want=("$@")

# THIS FLOW GAINS MORE FROM THE ALLOCATOR THAN THE PORTABILITY GATE DOES,
# because `synth_xilinx -flatten` is the heavier program: `KL_pp_shadow` runs
# 241.51 s under glibc and 171.00 s under jemalloc on one machine (-29.2%),
# reporting the same area row to the digit. Speed only, never results - #286
# proved the netlist byte-identical across glibc, tcmalloc, jemalloc and
# mimalloc, and the rows below are what this script exists to publish.
#
#   YOSYS_MALLOC=<path>   preload that library
#   YOSYS_MALLOC=none     run yosys under the system allocator
#   unset                 use jemalloc when it is installed
MALLOC_LIB="$(select_malloc)" || exit 2
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

# ...and with the processors come their ROMs. protocol_processor_top $readmemh's
# the ACMP listener transition image by the RELATIVE name "ltn_rom.hex", and
# KL_aecp_ucpu its microcode by "ucode.hex" (UCODE_HEX_P) -- yosys resolves
# both against ITS OWN working directory, and KL_gptp_ucpu reads
# "gptp_ucode.hex" the same way. Generate all three into $TMP and run yosys
# from an exclusive per-top directory below, so a run from the
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
#   - each image's CONTENT must match the sha256 recorded for its owning
#     processor pin in rom_digests.tsv: a correctly SHAPED wrong
#     image (a regressed generator emitting all-zero words) passed every
#     shape gate and priced KL_pp_shadow 4,045 LUT_TOT low ([R0] round two).
#     A pin bump re-records with --record-rom-digests, and that diff is
#     reviewed with the bump;
#   - each image is generated into an EXCLUSIVELY created staging file
#     (mktemp, never a predictable name a stale file could squat) and
#     published by a checked rename only after it validates; the published
#     target must be a regular file. OOC_TMP is reusable across runs;
#   - publication is not the end of custody ([R0] round four: a swap or
#     delete of the published image after validation, or between two tops,
#     still measured): each top's yosys run consumes an exclusive read-only
#     copy in a fresh unpredictable run directory, re-hashed against the
#     validated digest before AND after the run.
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
# The ucode depth is DERIVED (1 << UPC_W_C), so the exponent needs its own
# guard: positive_depth never sees it, and bash's shift is silent about every
# way it can go wrong. 0 makes the expected word count 1, which is exactly the
# one-word false green quoted in the header; 64 and 128 wrap back to 1; 63 is
# negative, so no image can ever match; and a leading-zero spelling ("08" is
# legal SystemVerilog decimal and pkg_num's (\d+) accepts it) is an octal
# arithmetic error that aborts the whole rom_spec word list before its first
# iteration, leaving the tops loop to die on an unset ROM_SHA key under set -u
# with no diagnostic of ours at all.
addr_width() { # <name> <value> -> value in 1..24, or die
  case "$2" in
    ''|*[!0-9]*|0?*) : ;;
    *) if [ "$2" -ge 1 ] && [ "$2" -le 24 ]; then printf '%s' "$2"; return 0; fi ;;
  esac
  echo "ooc.sh: FATAL: $1 = $2 is not a usable ROM address width (1..24, no leading zero) - the expected word count is 1 << $1, where 0 accepts a one-word image, >= 64 wraps bash's shift back to 1, and a leading zero is an octal arithmetic error" >&2
  exit 2
}
UCPU_PKG=$(one_pp_source ucpu_pkg.sv)     || exit 2
ACMP_PKG=$(one_pp_source pp_acmp_pkg.sv)  || exit 2
GPTP_UCPU_PKG="$R/gptp-processor/hdl/ucpu/gptp_ucpu_pkg.sv"
case " $GPTP_ENGINE_SRCS " in
  *" $GPTP_UCPU_PKG "*) : ;;
  *) echo "ooc.sh: FATAL: gPTP ROM geometry package is absent from the gPTP source population" >&2; exit 2 ;;
esac
[ -f "$GPTP_UCPU_PKG" ] || {
  echo "ooc.sh: FATAL: gPTP ROM geometry package is missing: $GPTP_UCPU_PKG" >&2
  exit 2
}
UCODE_W=$(pkg_num "$UCPU_PKG" UCODE_W_C)  || exit 2
UCODE_W=$(nibble_width UCODE_W_C "$UCODE_W") || exit 2
UPC_W=$(pkg_num "$UCPU_PKG" UPC_W_C)      || exit 2
UPC_W=$(addr_width UPC_W_C "$UPC_W")      || exit 2
TROM_W=$(pkg_num "$ACMP_PKG" TROM_W_C)    || exit 2
TROM_W=$(nibble_width TROM_W_C "$TROM_W") || exit 2
TROM_D=$(pkg_num "$ACMP_PKG" TROM_DEPTH_C) || exit 2
TROM_D=$(positive_depth TROM_DEPTH_C "$TROM_D") || exit 2
GPTP_UCODE_W=$(pkg_num "$GPTP_UCPU_PKG" UCODE_W_C) || exit 2
GPTP_UCODE_W=$(nibble_width GPTP_UCODE_W_C "$GPTP_UCODE_W") || exit 2
GPTP_UPC_W=$(pkg_num "$GPTP_UCPU_PKG" UPC_W_C) || exit 2
GPTP_UPC_W=$(addr_width GPTP_UPC_W_C "$GPTP_UPC_W") || exit 2

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

# The content ledger: sha256 per (owning processor pin, image), tracked.
# The pin is the SUPERPROJECT's gitlink, never the checkout's own HEAD
# ([R0] round five: a scratch checkout at another revision recorded and
# validated itself, and after an ordinary pin bump the retained old row
# would let a stale checkout price the wrong processor's HDL with a fully
# valid digest). The ONE reader below refuses an uninitialized, conflicted
# or mismatched checkout, in normal and record modes alike.
DIGESTS="$R/syn/yosys/rom_digests.tsv"
submodule_pin_of_record() { # <submodule>
  local name="$1" gitlink head
  if ! gitlink=$(git -C "$R" rev-parse ":$name" 2>/dev/null); then
    echo "ooc.sh: FATAL: cannot read the $name gitlink from the superproject index (a missing or conflicted gitlink has no one revision to key the ledger by)" >&2
    return 2
  fi
  if ! head=$(git -C "$R/$name" rev-parse HEAD 2>/dev/null); then
    echo "ooc.sh: FATAL: the $name submodule is not checked out - git submodule update --init $name" >&2
    return 2
  fi
  if [ "$head" != "$gitlink" ]; then
    echo "ooc.sh: FATAL: the $name checkout ($head) disagrees with the superproject pin ($gitlink) - a stale checkout generates another processor's ROMs however valid its own digests look; run git submodule update" >&2
    return 2
  fi
  printf '%s' "$gitlink"
}
pp_pin_of_record() { submodule_pin_of_record protocol-processor; }
gptp_pin_of_record() { submodule_pin_of_record gptp-processor; }
PP_PIN=$(pp_pin_of_record) || exit 2
GPTP_PIN=$(gptp_pin_of_record) || exit 2

# The digest each image VALIDATED at, kept for consumption ([R0] round
# four): validation bound the ledger to the staged bytes, but yosys then
# consumed the shared published pathname unchecked, so a swap or delete
# after publication (or between two tops) still measured. Every consumption
# below re-hashes the exact copy yosys will read against this record.
declare -A ROM_SHA
copy_matches() { # <file> <image name> -> 0 iff sha256 equals the validated digest
  local got
  # The status is TAKEN and the pipe is gone: `sha256sum | awk` hands back
  # awk's status, so a sha256sum that never ran produced an empty string that
  # only happened to compare unequal. An empty digest is a failure to measure,
  # never a measurement, so it is refused explicitly.
  got=$(sha256sum < "$1" 2>/dev/null) || return 1
  got=${got%% *}
  [ ${#got} -eq 64 ] || return 1
  [ "$got" = "${ROM_SHA[$2]}" ]
}

new_rows=""
for rom_spec in \
    "ltn_rom.hex|$R/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py|$TROM_W|$TROM_D|$PP_PIN|protocol-processor" \
    "ucode.hex|$R/protocol-processor/hdl/aecp/ucode/gen_ucode.py|$UCODE_W|$((1 << UPC_W))|$PP_PIN|protocol-processor" \
    "gptp_ucode.hex|$R/gptp-processor/hdl/ucode/gen_gptp_ucode.py|$GPTP_UCODE_W|$((1 << GPTP_UPC_W))|$GPTP_PIN|gptp-processor"; do
  IFS='|' read -r img gen width depth pin pin_name <<< "$rom_spec"
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
  # This is the value RECORD mode writes into a tracked file, so its status is
  # taken here too: `$(sha256sum | awk)` reported awk's status, and an empty
  # digest was recorded verbatim as if it were one - a blank third column that
  # then refuses every later run at the pin it was just recorded for.
  if ! got=$(sha256sum < "$stage"); then
    rm -f "$stage"
    echo "ooc.sh: FATAL: cannot hash the staged $img - a digest this script did not compute must never be recorded or compared" >&2
    exit 2
  fi
  got=${got%% *}
  if [ ${#got} -ne 64 ]; then
    rm -f "$stage"
    echo "ooc.sh: FATAL: sha256sum produced no usable digest for $img ('$got')" >&2
    exit 2
  fi
  ROM_SHA[$img]="$got"
  if [ "$RECORD" -eq 1 ]; then
    new_rows="${new_rows}${pin}	${img}	${got}
"
  else
    # `recorded`, not `want`: `want` is the requested-tops ARRAY above.
    recorded=$(awk -v p="$pin" -v i="$img" '$1 == p && $2 == i { print $3; exit }' "$DIGESTS" 2>/dev/null)
    if [ -z "$recorded" ]; then
      rm -f "$stage"
      echo "ooc.sh: FATAL: no recorded content digest for $img at $pin_name pin $pin in syn/yosys/rom_digests.tsv - a pin bump re-records with ./ooc.sh --record-rom-digests, and that diff is reviewed with the bump" >&2
      exit 2
    fi
    if [ "$got" != "$recorded" ]; then
      rm -f "$stage"
      echo "ooc.sh: FATAL: content digest mismatch for $img at $pin_name pin $pin: generated $got, recorded $recorded - the generator regressed (a correctly shaped wrong image still prices wrong) or the ledger is stale" >&2
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
  # Rewrite both owning pins' rows, keep every other pin's, keep the header.
  #
  # NEVER PIPE A GATE, least of all a DESTRUCTIVE one. The old spelling tested
  # `sort`'s status only: a dying awk (or a momentarily unreadable ledger, both
  # greps being 2>/dev/null) produced an EMPTY retained body while sort exited
  # 0, the rename installed a ledger holding nothing but the current rows,
  # and the run printed "recorded ROM content digests" and exited 0. Every
  # other pin's digests were silently deleted from a tracked file, and the
  # bump's reviewer saw deletions that read as a deliberate prune.
  header=""
  kept=""
  if [ -e "$DIGESTS" ]; then
    header=$(grep -h '^#' "$DIGESTS") || [ $? -eq 1 ] || {
      echo "ooc.sh: FATAL: cannot read syn/yosys/rom_digests.tsv - refusing to rewrite a ledger whose header was never read" >&2
      exit 2; }
    body=$(grep -hv '^#' "$DIGESTS") || [ $? -eq 1 ] || {
      echo "ooc.sh: FATAL: cannot read syn/yosys/rom_digests.tsv - refusing to rewrite a ledger whose existing rows were never read" >&2
      exit 2; }
    if [ -n "$body" ]; then
      kept=$(printf '%s\n' "$body" | awk -v p="$PP_PIN" -v g="$GPTP_PIN" \
          '$1 != p && $1 != g') || {
        echo "ooc.sh: FATAL: cannot select the rows to retain from syn/yosys/rom_digests.tsv - refusing to rewrite a ledger whose other pins were never read" >&2
        exit 2; }
    fi
  fi
  # An explicit count is the anti-truncation oracle: what goes out must be the
  # rows retained plus the rows recorded, and nothing less.
  kept_n=0; [ -z "$kept" ] || kept_n=$(printf '%s\n' "$kept" | grep -c .)
  new_n=$(printf '%s' "$new_rows" | grep -c .)
  if ! LEDGER_STAGE=$(mktemp "$DIGESTS.new.XXXXXXXX"); then
    echo "ooc.sh: FATAL: cannot create an exclusive staging file for syn/yosys/rom_digests.tsv" >&2
    exit 2
  fi
  {
    [ -z "$header" ] || printf '%s\n' "$header"
    { [ -z "$kept" ] || printf '%s\n' "$kept"
      printf '%s' "$new_rows"; } | LC_ALL=C sort
  } > "$LEDGER_STAGE" || {
    echo "ooc.sh: FATAL: cannot write the new syn/yosys/rom_digests.tsv" >&2
    exit 2; }
  out_n=$(grep -cv '^#' "$LEDGER_STAGE") || [ $? -eq 1 ] || out_n=-1
  if [ "$out_n" -ne $(( kept_n + new_n )) ]; then
    echo "ooc.sh: FATAL: the rewritten ledger holds $out_n row(s), expected $(( kept_n + new_n )) ($kept_n retained + $new_n recorded) - refusing to install a ledger that lost another pin's digests" >&2
    exit 2
  fi
  if ! mv "$LEDGER_STAGE" "$DIGESTS"; then
    echo "ooc.sh: FATAL: cannot install the new syn/yosys/rom_digests.tsv" >&2
    exit 2
  fi
  LEDGER_STAGE=""
  echo "ooc.sh: recorded ROM content digests for protocol-processor pin $PP_PIN and gptp-processor pin $GPTP_PIN in syn/yosys/rom_digests.tsv"
  exit 0
fi
status=0
printf "== OOC area (synth_xilinx -family xc7 -flatten) ==\n"
# Named, because a wall-clock figure quoted beside these rows is only
# reproducible if the allocator that produced it is on the record (#290).
printf "   yosys allocator: %s\n" "${MALLOC_LIB:-system}"
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
  # The status is taken here for the same reason it is taken on the ROM
  # publish target: a directory squatting this path makes `rm -f` fail, and
  # `[ -s DIR ]` is TRUE, so the report gate below would have accepted a
  # directory as "the netlist artifact exists".
  if ! rm -f "$TMP/$top.ooc.json"; then
    echo "ooc.sh: FATAL: cannot remove the previous $top.ooc.json in $TMP (a directory or unwritable entry is squatting the artifact the report gate tests)" >&2
    exit 2
  fi
  # [R0] round four: synthesis consumes an EXCLUSIVE per-top copy of each
  # validated image, never the shared published pathname. The run directory
  # is a fresh mktemp -d (mode 0700, unpredictable name), each copy is
  # re-hashed against the validated digest (the hash binds the exact file
  # yosys reads), made read-only, and re-hashed AGAIN after yosys returns:
  # no row survives bytes that disappeared or changed at any point around
  # the run, however plausible the stat block looks.
  if ! rundir=$(mktemp -d "$TMP/$top.run.XXXXXXXX"); then
    echo "ooc.sh: FATAL: cannot create an exclusive run directory for $top in $TMP" >&2
    exit 2
  fi
  RUNDIR="$rundir"   # the EXIT trap unlocks and removes it on every path
  for img in ucode.hex ltn_rom.hex gptp_ucode.hex; do
    if ! cp "$TMP/$img" "$rundir/$img"; then
      echo "ooc.sh: FATAL: $img is gone from $TMP after validation, or could not be copied (cp's own error is above: a writer reached the published image, or the filesystem is full) - refusing to synthesize $top against bytes no ledger row vouches for" >&2
      exit 2
    fi
    if ! chmod a-w "$rundir/$img"; then
      echo "ooc.sh: FATAL: cannot make the consuming copy of $img read-only for $top - an ignored chmod is an open write seam, not a hardening" >&2
      exit 2
    fi
  done
  # [R0] round five: file permission alone is NOT immutability - rename
  # authority is DIRECTORY write permission, so a writer could move the
  # reviewed file aside, feed yosys different bytes, and restore the
  # reviewed file before the post-run hash with both hashes green. The run
  # directory is therefore locked (u-w) BEFORE the copies are hashed and
  # stays locked through the post-run re-hash: the hashes bind names that
  # can no longer be rebound, for the whole read interval.
  if ! chmod u-w "$rundir"; then
    echo "ooc.sh: FATAL: cannot make $top's run directory read-only - rename authority is directory write permission, and an open interval is exactly the transient-swap seam" >&2
    exit 2
  fi
  for img in ucode.hex ltn_rom.hex gptp_ucode.hex; do
    if ! copy_matches "$rundir/$img" "$img"; then
      echo "ooc.sh: FATAL: $img changed after publication - the consuming copy for $top no longer hashes to the validated digest; refusing to measure bytes no ledger row vouches for" >&2
      exit 2
    fi
  done
  # apply_malloc_env is INSIDE the subshell, so the preload reaches yosys and
  # the abc it spawns and dies with them: sv2v and the python3 ROM generators
  # above were not measured under a replacement allocator and keep the caller's
  # environment. The opening of the line below - `(cd "$rundir" &&` followed
  # by the apply_malloc_env call - is load-bearing: the cwd-escape and
  # consume-shared-dir arms of ooc_selftest.py plant their mutations on
  # exactly that text (and refuse if it appears twice, so do not quote it
  # verbatim here), and its allocator arms read the model's record of what
  # yosys and sv2v ran under.
  (cd "$rundir" && apply_malloc_env "$MALLOC_LIB" && yosys -p "read_verilog $TMP/$top.ooc.v;$chp synth_xilinx -family xc7$nodsp -top $top -flatten; stat; write_json $TMP/$top.ooc.json") \
    > "$TMP/$top.ooc.log" 2>&1
  yosys_rc=$?
  for img in ucode.hex ltn_rom.hex gptp_ucode.hex; do
    if ! copy_matches "$rundir/$img" "$img"; then
      echo "ooc.sh: FATAL: $img changed under $top's synthesis run - the read-only consuming copy no longer hashes to the validated digest; discarding whatever was measured" >&2
      exit 2
    fi
  done
  if ! chmod u+w "$rundir"; then
    echo "ooc.sh: FATAL: cannot unlock $top's run directory for cleanup" >&2
    exit 2
  fi
  rm -rf "$rundir"
  RUNDIR=""
  if [ "$yosys_rc" -ne 0 ]; then
    printf "%-28s yosys FAIL: %s\n" "$top" "$(grep -oE 'ERROR:.*' "$TMP/$top.ooc.log" | head -1)"; status=1; continue
  fi
  # yosys said 0; the REPORT phase must fail closed too ([R-parallel] on
  # #245): the JSON artifact the command names must exist non-empty (its
  # absence means the netlist was never written, whatever the log says), and
  # the row must come from a real parsed stat block, never be manufactured by
  # an END clause over an empty parse.
  if ! [ -f "$TMP/$top.ooc.json" ] || [ -L "$TMP/$top.ooc.json" ] \
     || ! [ -s "$TMP/$top.ooc.json" ]; then
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
  # UG474 (7 Series CLB). The table below covers EVERY RAM<n>... primitive
  # yosys's own Xilinx cell library can emit (/usr/share/yosys/xilinx), and an
  # unrecognised one is a REFUSAL, not a zero: `return 0` for an unnamed cell
  # is the identical silent under-count this column was added to stop, and it
  # was reachable - the _1 (negative write-clock) variants, RAM256X1D and
  # RAM512X1S all fell through the old eleven-name table and priced free.
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
      if (t == "RAM256X1D" || t == "RAM512X1S" || t == "RAM32X8S" ||
          t == "RAM64X8SW" || t == "RAM32X16DR8") return 8;
      if (t == "RAM32M" || t == "RAM64M" || t == "RAM128X1D" ||
          t == "RAM32M16" || t == "RAM64M8" || t == "RAM256X1S" ||
          t == "RAM32X4S") return 4;
      if (t == "RAM32X1D" || t == "RAM32X1D_1" || t == "RAM64X1D" ||
          t == "RAM64X1D_1" || t == "RAM128X1S" || t == "RAM128X1S_1" ||
          t == "RAM32X2S" || t == "RAM64X2S") return 2;
      if (t == "RAM32X1S" || t == "RAM32X1S_1" ||
          t == "RAM64X1S" || t == "RAM64X1S_1") return 1;
      return 0;
    }
    /^=== .* ===$/ { inblk = 0 }
    $0 == "=== " top " ===" { blocks++; inblk=1; lut=0; lrm=0; ff=0; r36=0; r18=0; dsp=0; c4=0 }
    inblk && $2 ~ /^LUT[1-6]$/     { lut += $1 }
    inblk && $2 ~ /^RAM[0-9]/      { c = lram_luts($2)
                                     if (c == 0) unpriced = $2
                                     lrm += $1 * c }
    inblk && $2 ~ /^FD[CPRS]E?$/   { ff  += $1 }
    inblk && $2 ~ /^RAMB36E1$/     { r36 += $1 }
    inblk && $2 ~ /^RAMB18E1$/     { r18 += $1 }
    inblk && $2 ~ /^DSP48E1$/      { dsp += $1 }
    inblk && $2 ~ /^CARRY4$/       { c4  += $1 }
    END {
      if (blocks == 0) { printf "no stat block for %s in the log", top; exit 3 }
      if (unpriced != "") {
        printf "distributed-RAM cell %s carries no LUT6 cost in this parser - pricing it free is exactly the under-count the LUTRAM column exists to stop; add its UG474 SLICEM occupancy", unpriced
        exit 5
      }
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
# Cleanup is the EXIT trap's (one place, every path). It must not launder a
# failed top back into success either: exit with the accumulated verdict, not
# with the last statement's (#245).
exit "$status"
