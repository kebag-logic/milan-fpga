#!/bin/bash
# build.sh - named-config bitstream launcher for the Milan SoC (two-board lab).
#
# usage:
#   ./build.sh <config> [<config> ...] [--sweep] [--dry-run] [-- <extra milan_soc.py args>]
#
#   ./build.sh ax7101                  # ship shape (cbsf lineage) -> work/build_ax7101_<tag>
#   ./build.sh arty                    # Arty A7-100 bring-up shape
#   ./build.sh ax7101 arty             # BOTH boards, parallel, 90 s stagger
#   ./build.sh --sweep ax7101          # 3-directive place sweep (epo/spr/etm), per the
#                                      # saturate-the-box rule (3 x 32 threads)
#   TAG=myrun ./build.sh arty          # output dir suffix (default: date +%m%d%H%M)
#   ./build.sh arty -- --sys-clk-freq 90e6   # append/override milan_soc.py args
#
# Discipline encoded here (docs/integration/BUILDING.md):
#   * every build: setsid nohup (harness task-kills must never reap Vivado),
#     --vivado-max-threads 32 (Vivado hard cap), launch log next to the outdir;
#   * parallel launches staggered 90 s (shared pythondata git checkout: two
#     concurrent LiteX elaborations race on index.lock and crash);
#   * at most 3 concurrent builds (3 x 32 = the 96-core box saturated).
#
# Configs are FUNCTIONS below - one place to edit a board's canonical shape.
# MAINTAINER DOC: docs/integration/BUILDING.md (configs, discipline rationale, per-board
# load/console facts, gates). Update it when adding a config or a rule here.

set -euo pipefail
WORK=$HOME/litex-milan/work
SOC_DIR="$(cd "$(dirname "$0")" && pwd)"
TAG=${TAG:-$(date +%m%d%H%M)}
STAGGER=90
REPO_ROOT="$(cd "$SOC_DIR/../.." && pwd)"

# ---- per-board flash/JTAG facts (docs/integration/BUILDING.md section 4) --------------------
# serial = FTDI serial (TWO cables on the bus: NEVER omit, a flash op picking the
# wrong board is destructive). Serials are BENCH-LOCAL: set AX_FTDI/ARTY_FTDI in
# the environment or in sw/litex/boards.local.sh (gitignored; template =
# boards.local.sh.example). policy = what this board's QSPI holds:
#   both boards "boot" (USER 2026-07-20: "to flash use qspi"): bitstream at
#   offset 0 in a dedicated 4 MiB slot, followed by the profile-selected
#   images from flashboot_layout.json. The shipping AX shape stores its raw
#   AEM image at 4 MiB; Linux bring-up shapes retain the kernel/OpenSBI/DTB/
#   rootfs layout.
#   The historical "AX bitstream = kernel-clobber trap" note described the OLD
#   kernel-at-offset-0 layout and died with the manifest-"full" port.
[ -f "$SOC_DIR/boards.local.sh" ] && . "$SOC_DIR/boards.local.sh"
AX_FTDI="${AX_FTDI:-SET_AX_FTDI}"       # sentinel fails loudly in openFPGALoader
ARTY_FTDI="${ARTY_FTDI:-SET_ARTY_FTDI}"
board_facts() {  # -> "serial cable fpga_part flash_policy bit_name"
    case "$1" in
        ax7101) echo "$AX_FTDI ft232    xc7a100tfgg484 boot      alinx_ax7101.bit";;
        arty)   echo "$ARTY_FTDI digilent xc7a100tcsg324 boot      digilent_arty.bit";;
        *)      return 1;;
    esac
}

# ---- flash subcommand: ./build.sh flash <config>[:<builddir>] ... ---------------
# ax7101 -> deploy.sh flash-images (FBI wrap + per-image budget checks + --verify);
#           needs KERNEL/OPENSBI/DTB/ROOTFS=<path> in the environment per the
#           layout's manifest. arty -> bitstream to QSPI offset 0 with --verify.
if [ "${1:-}" = "flash" ]; then
    shift
    [ $# -gt 0 ] || { echo "usage: $0 flash <config>[:<builddir>] ..." >&2; exit 2; }
    for spec in "$@"; do
        c=${spec%%:*}; dir=${spec#*:}; [ "$dir" = "$spec" ] && dir=""
        facts=$(board_facts "$c") || { echo "unknown board config '$c'" >&2; exit 2; }
        read -r serial cable part policy bitname <<<"$facts"
        if [ -z "$dir" ]; then
            # newest build dir containing the artifact this policy flashes
            # (|| true: an empty glob must reach the friendly error, not set -e)
            # boot/bitstream discover by the bit (json is reconstructed below if absent)
            want="flashboot_layout.json"; case "$policy" in bitstream|boot) want="gateware/$bitname";; esac
            dir=$( { ls -td "$WORK"/build_${c}*/ 2>/dev/null || true; } | while read -r d; do
                      [ -f "$d/$want" ] && { echo "$d"; break; }; done || true)
            [ -n "$dir" ] || { echo "[$c] no build containing $want under $WORK/build_${c}* (pass ${c}:<builddir>)" >&2; exit 2; }
        else
            case "$dir" in /*) ;; *) dir="$WORK/$dir";; esac
        fi
        dir=${dir%/}
        # sweep builds skip main()'s json export; reconstruct from the compiled
        # BIOS constants (soc.h is the single source of truth either way)
        if [ ! -f "$dir/flashboot_layout.json" ] && [ -f "$dir/software/include/generated/soc.h" ]; then
            "${PYTHON:-python3}" "$SOC_DIR/layout_from_soch.py" "$dir"
        fi
        case "$policy" in
            boot)
                # v3 QSPI-boot: gateware @0 THEN the image set (shifted offsets).
                bit="$dir/gateware/$bitname"
                [ -f "$bit" ] || { echo "[$c] missing $bit" >&2; exit 2; }
                echo "== flash [$c] BITSTREAM @0 =="
                out=$(openFPGALoader --ftdi-serial "$serial" -c "$cable" --fpga-part "$part" -f --verify "$bit" 2>&1) \
                    || { echo "$out"; exit 1; }
                echo "$out" | grep -qiE "error|can.t program" && { echo "[$c] BIT FLASH FAILED"; exit 1; }
                echo "== flash [$c] IMAGES (v3 layout offsets) =="
                SERIAL="$serial" CABLE="$cable" FPGA_PART="$part" \
                    LAYOUT="$dir/flashboot_layout.json" "$SOC_DIR/deploy.sh" flash-images
                echo "   done. Power-cycle to boot gateware + its paired firmware images from QSPI."
                ;;
            images)
                echo "== flash [$c] IMAGES -> QSPI (layout offsets; bitstream stays JTAG-SRAM) =="
                SERIAL="$serial" CABLE="$cable" FPGA_PART="$part" \
                    LAYOUT="$dir/flashboot_layout.json" "$SOC_DIR/deploy.sh" flash-images
                ;;
            bitstream)
                bit="$dir/gateware/$bitname"
                [ -f "$bit" ] || { echo "[$c] missing $bit" >&2; exit 2; }
                echo "== flash [$c] BITSTREAM -> QSPI offset 0 (self-configures on power-up) =="
                echo "   $bit"
                # --fpga-part: the SPI proxy needs the device-package (openFPGALoader
                # cannot infer it for every cable profile, and exits 0 on the miss)
                out=$(openFPGALoader --ftdi-serial "$serial" -c "$cable" --fpga-part "$part" -f --verify "$bit" 2>&1) || { echo "$out"; exit 1; }
                echo "$out" | tail -3
                echo "$out" | grep -qiE "error|can't program" && { echo "[$c] FLASH FAILED"; exit 1; }
                echo "   done. Power-cycle (or --reset) to boot the flashed gateware."
                ;;
        esac
    done
    exit 0
fi

# ---- named configurations -----------------------------------------------------
cfg_ax7101() {   # shipping bare-metal shape: one cacheless RV32I hart. Linux
                 # and the prior cached VexiiRiscv configurations remain in
                 # cfg_ax8x8/cfg_arty as explicit bring-up profiles.
    # BODY = the tdm8 internal-COMPLIANCE/ship set (byte-matched to the t529 sweep Command;
    # the nic-perf RV64 revision below had leaked back in as the bare body,
    # so an extras-less `--sweep ax7101` built prefetch-rpt/l2-16K/no-tdm8 -
    # the whole t530 sweep was that wrong SoC, +11.5k LUTs, unplaceable).
    # nic-perf revision (dormant, launch WITH extras if ever needed):
    #   --l2-bytes 16384 --scala-args=--lsu-l1-refill-count=8
    #   --scala-args=--lsu-hardware-prefetch=rpt
    #   --scala-args=--l2-down-pending=8 --scala-args=--l2-general-slots=16
    echo "--board ax7101 --cpu vexiiriscv --cpu-count 1 --xlen 32 \
          --software-profile baremetal --all-blocks --coherent-dma \
          --milan-clk-freq 50e6 --with-spiflash --flashboot baremetal \
          --gtx-tx-invert --timing-opt --floorplan --eth-port e1 \
          --no-i2s-playback --no-render-lpf --audio-interface tdm8 \
          --audio-interface-master --talker-wire-chans 8 --cbs-queues-mask 0x10 \
          --loopback-lane --fabric-gptp \
          --entity-gen-dir $SOC_DIR/../../configs/generated/endstation_ax7101_1x1_tdm8 \
          --synth-directive AreaOptimized_high --opt-directive ExploreArea \
          --l2-bytes 0 \
          --uart-baudrate 115200 --rx-queues 2 --strip-probes --hs-page-bytes 16384 \
          --place-directive ExtraPostPlacementOpt"
}
cfg_ax8x8() {    # 8-stream (64ch) shape. History: the 07-24 close used
                 # --rx-queues 1 (dropping the RX1 DMA RSC engine removed the
                 # sys_clk critical path and freed ~3% LUT) - but D7 ended
                 # that option on 2026-07-28: with one queue there is no
                 # flow-steer block, ptp4l shares the bulk ring, and under a
                 # 950M flood our GM starves and a conformant BMCA deposes it
                 # (docs/findings/GPTP_GM_LOSS_UNDER_RX_LOAD.md, 2/2). So
                 # rx-queues is 2 NOW, non-negotiable, and the area it costs
                 # is why the 0x0019 round spends the tier-1 prunes below.
                 # The other 07-24 move stands: default (timing) synth
                 # instead of the blunt AreaOptimized flag. The remaining -0.155 was a FALSE path
                 # (cap_luid_r -> shared ctx read mux -> ACMP sweep writeback,
                 # impossible: sweep write needs !w_frame_latch) fixed in RTL by
                 # a dedicated sweep read port in the then-current ACMP listener
                 # context (deleted 2026-08-13 with the legacy plane). Result
                 # 2026-07-24: WNS +0.080, LUT 85.15%, TNS 0 (all seeds close).
    echo "--board ax7101 --cpu vexiiriscv --cpu-count 1 --software-profile linux \
          --all-blocks --coherent-dma --sound-card \
          --milan-clk-freq 100e6 --with-spiflash --flashboot full --gtx-tx-invert \
          --timing-opt --floorplan --l2-bytes 16384 \
          --scala-args=--lsu-l1-refill-count=8 --scala-args=--lsu-hardware-prefetch=rpt \
          --uart-baudrate 115200 --rx-queues 2 --strip-probes --hs-page-bytes 16384 \
          --num-streams 8 --audio-interface tdm32 --audio-interface-master \
          --talker-wire-chans 8 --no-latency-taps --no-i2s-playback \
          --aaf-playback --no-fabric-gptp --xlen 64 \
          --entity-gen-dir $SOC_DIR/../../configs/generated/endstation_ax7101_8x8 \
          --no-render-lpf --cbs-queues-mask 0x18 --synth-directive AreaOptimized_high \
          --opt-directive ExploreArea --place-directive AltSpreadLogic_high"
                 # --no-fabric-gptp: this profile is Linux, its rootfs still
                 # starts ptp4l, and the PHC takes exactly ONE owner. Stated
                 # rather than left to the default so the recipe and
                 # configs/endstation_ax7101_8x8.yaml carry the same fact;
                 # check_sweep_shape.py compares the two flag for flag.
                 # --entity-gen-dir: the descriptor image, the platform shape
                 # and (on a fabric build) the gPTP ROM all come from the
                 # config named in ENTITY_CFG_ax8x8 below. Without it
                 # milan_soc.py refuses the launch, so this recipe could not
                 # be run at all.
                 # --xlen 64 STATES WHAT THIS RECIPE ALREADY BUILDS. The flag
                 # was absent and milan_soc.py defaults it to 64, so nothing
                 # about the elaborated SoC moves; what moves is that the
                 # value is now readable here, beside a config that declares
                 # xlen 32. WHICH SIDE IS RIGHT IS NOT DECIDED HERE and must
                 # not be guessed: see issue #157. Until it closes, the pair
                 # is pinned in scripts/check_sweep_shape.py so neither end
                 # can move quietly.
                 # --aaf-playback (task #31, 2026-08-02) = KL_pcm_tx host
                 # playback ring -> the chmap capture RING bucket: the ALSA
                 # playback direction (snd-kl-milan pb-dma window; DT
                 # kl,playback-streams). ONE ring served (the START-SMALL
                 # --aaf-playback-streams default; full-N OOC'd 2216 LUT,
                 # one-ring ~1/8th) - its 4 pairs reach any talker's wire
                 # slots through the 64ch chmap. The render sample bank
                 # behind it is unloaded on this padless board and sweeps.
                 # --no-render-lpf = the SPENT LPF_P area lever (2026-07-27,
                 # docs/design/AREA_BUDGET.md). 428 LUT / 756 FF / 0 DSP
                 # from the shipping 8x8 place report - the only Vivado-PROVEN
                 # figure of that round - on the board whose 6-queue map missed
                 # placement by 282 slices. Pruned, the render tap behaves
                 # exactly like LPF_CTRL[0]=0 does today (raw AXIS to the DAC),
                 # so no CSR and no digital acceptance surface moves; the analog
                 # loop THD+N record, however, was measured THROUGH the filter
                 # and must be re-measured before it is quoted against this
                 # bitstream. Drop the flag to put the filter back.
                 # eth-port defaults to e1 (the bench default, same as cfg_ax7101).
                 # If the AX cable is on e2, append `-- --eth-port e2`; AX42's guard
                 # reset scope covers either PHY's tx/gtx path.
}
cfg_arty() {     # Arty A7-100 small endstation: MII 100M, QSPI flashboot (probes stripped since v8 - AVDECC stack needs the slices: v7-style probes overflowed by 181)
    # -1 die: 100 MHz datapath does NOT close (measured -1.0 WNS); 50 MHz is
    # 3.2 Gb/s of 64-bit datapath for a 100 Mbit wire. sys 83.333 = the clean
    # PLL divisor set (VCO 1000; 90e6 has NO solution with the 25 MHz eth ref).
    # Flash = bitstream@0 + the full-manifest Linux images (QSPI self-boot on
    # both boards; the old kernel-at-0 / JTAG-SRAM-only layout died with the
    # manifest-full port - see board_facts above + docs/integration/QSPI_FLASHBOOT.md).
    echo "--board arty --cpu vexiiriscv --cpu-count 2 --software-profile linux \
          --all-blocks --coherent-dma --sound-card \
          --sys-clk-freq 83.333e6 --milan-clk-freq 50e6 --with-spiflash --flashboot full \
          --uart-baudrate 115200 --timing-opt --strip-probes --l2-bytes 65536 \
          --scala-args=--lsu-l1-refill-count=8 --scala-args=--lsu-hardware-prefetch=rpt \
          --scala-args=--l2-down-pending=8 --scala-args=--l2-general-slots=16 \
          --rx-queues 2 --hs-page-bytes 16384 --no-fabric-gptp --xlen 64 \
          --entity-gen-dir $SOC_DIR/../../configs/generated/endstation_arty_current"
                 # --no-fabric-gptp / --entity-gen-dir / --xlen 64: same three
                 # reasons as cfg_ax8x8 above. Linux profile, one PHC owner,
                 # the config named in ENTITY_CFG_arty supplies the descriptor
                 # image and platform shape this build cannot start without,
                 # and the RV64 the absent --xlen already selected is now
                 # written down rather than inherited. This recipe also states
                 # --cpu-count 2 where the config declares 1, and sweep.sh's
                 # arty leg states RV32 with one hart. Three artifacts, two
                 # answers: issue #157.
}

SWEEP_DIRECTIVES="ExtraPostPlacementOpt AltSpreadLogic_high ExtraTimingOpt"

# ---- arg parsing ----------------------------------------------------------------
CONFIGS=(); SWEEP=0; DRY=0; EXTRA=()
while [ $# -gt 0 ]; do
    case "$1" in
        --sweep)   SWEEP=1;;
        --dry-run) DRY=1;;
        --)        shift; EXTRA=("$@"); break;;
        *)         type "cfg_$1" >/dev/null 2>&1 || { echo "unknown config '$1' (have: $(declare -F | sed -n 's/.* cfg_/ /p' | tr -d '\n'))" >&2; exit 2; }
                   CONFIGS+=("$1");;
    esac
    shift
done
[ ${#CONFIGS[@]} -gt 0 ] || { echo "usage: $0 <config> [<config> ...] [--sweep] [--dry-run] [-- extra args]" >&2; exit 2; }

# ---- entity-definition gate (HARD, not advisory) --------------------------------
# The gateware `include-s a GENERATED entity definition: the ADPDU stream counts
# in hdl/common/csr/gen/adp_shape_defaults.svh, served read-only at 0x618/0x61C
# and ALSO sizing the protocol processor's ACMP source/sink context arrays. It
# comes from ONE end-station config via endstation_builder.py --write-rtl.
# Until 2026-07-27 nothing checked WHICH config: the tree carried the 1x1 shape
# and every build, 8x8 included, compiled it in - so the 8x8 board advertised 1
# talker source. Refuse to launch if the tree is another shape's.
# (The AEM descriptor ROM used to be the second half of this gate, and briefly
#  had no successor: the deleted AECP/AEM engine took the in-gateware ROM with
#  it. The descriptors are back, in DRAM - milan_soc.py builds the image for
#  THIS config from the same out/ directory and writes it beside the bitstream,
#  refusing to launch Vivado if the model is missing or unbuildable. So the
#  shape check below still covers only the `svh`; the descriptors now police
#  themselves, per build, and cannot be another config's.)
ENTITY_CFG_ax8x8="configs/endstation_ax7101_8x8.yaml"
ENTITY_CFG_arty="configs/endstation_arty_current.yaml"
for c in "${CONFIGS[@]}"; do
    eval "ecfg=\${ENTITY_CFG_$c:-}"
    [ -n "$ecfg" ] || continue
    python3 "$REPO_ROOT/scripts/check_entity_shape.py" --built-config "$REPO_ROOT/$ecfg" \
        || { echo "refusing to build '$c': the tracked entity definition is not $ecfg's" >&2; exit 2; }
done

# ---- expand configs (x directives when sweeping) --------------------------------
JOBS=()   # "name|args"
for c in "${CONFIGS[@]}"; do
    base_args=$("cfg_$c")
    if [ "$SWEEP" = 1 ]; then
        for d in $SWEEP_DIRECTIVES; do
            short=$(echo "$d" | tr -dc 'A-Z' | tr 'A-Z' 'a-z')
            # strip any config-default place directive, then pin the sweep's
            args=$(echo "$base_args" | sed 's/--place-directive [A-Za-z_]*//')
            JOBS+=("${c}_${short}|$args --place-directive $d")
        done
    else
        JOBS+=("${c}|$base_args")
    fi
done
[ ${#JOBS[@]} -le 3 ] || { echo "refusing ${#JOBS[@]} parallel builds (box saturates at 3 x 32 threads); split the call" >&2; exit 2; }

# ---- launch ---------------------------------------------------------------------
first=1
for job in "${JOBS[@]}"; do
    name=${job%%|*}; args=${job#*|}
    out="$WORK/build_${name}_${TAG}"
    cmd="cd $SOC_DIR && source $HOME/Xilinx2/2026.1/Vivado/settings64.sh && \
         export PATH=$HOME/litex-milan/venv/bin:\$PATH && \
         exec python3 milan_soc.py $args ${EXTRA[*]:-} --vivado-max-threads 32 --build --output-dir $out"
    if [ "$DRY" = 1 ]; then
        echo "DRY [$name] -> $out"; echo "  $cmd" | tr -s ' '; continue
    fi
    [ "$first" = 1 ] || { echo "stagger ${STAGGER}s (shared pythondata checkout)"; sleep $STAGGER; }
    first=0
    setsid nohup bash -c "$cmd" > "$WORK/build_${name}_${TAG}.launch.log" 2>&1 &
    echo "LAUNCHED [$name] pid=$! out=$out log=$WORK/build_${name}_${TAG}.launch.log"
done
