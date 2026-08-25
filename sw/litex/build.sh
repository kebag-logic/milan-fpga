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
#   offset 0 in a dedicated 4 MiB slot, followed by the raw AEM image at
#   4 MiB per flashboot_layout.json. Every named config is bare-metal (#259);
#   the retired Linux kernel/OpenSBI/DTB/rootfs manifests are historical and
#   no recipe here emits them.
#   The historical "AX bitstream = kernel-clobber trap" note described the OLD
#   kernel-at-offset-0 layout and died with the manifest-"full" port.
[ -f "$SOC_DIR/boards.local.sh" ] && . "$SOC_DIR/boards.local.sh"
AX_FTDI="${AX_FTDI:-SET_AX_FTDI}"       # sentinel fails loudly in openFPGALoader
ARTY_FTDI="${ARTY_FTDI:-SET_ARTY_FTDI}"
board_facts() {  # -> "serial cable fpga_part flash_policy bit_name"
    case "$1" in
        ax7101|ax8x8) echo "$AX_FTDI ft232    xc7a100tfgg484 boot      alinx_ax7101.bit";;
        arty)          echo "$ARTY_FTDI digilent xc7a100tcsg324 boot      digilent_arty.bit";;
        *)      return 1;;
    esac
}
gptp_owner_for_config() {
    # #259: the fabric plane is the ONE gPTP owner; the software owner is
    # retired, so no named config may expect it.
    case "$1" in
        ax7101|ax8x8|arty) echo fabric;;
        *)          return 1;;
    esac
}

# ---- flash subcommand: ./build.sh flash <config>[:<builddir>] ... ---------------
# Every persistent named-config write delegates to deploy.sh flash-pair. Supply
# INSTALLED_LAYOUT + INSTALLED_BIT for the exact build currently in the board's
# QSPI (or INSTALLED_BUILD=<dir> to derive both). The transaction proves that
# bitstream by live readback, prepares the whole target set, then selects the
# direction-safe verified write order.
if [ "${1:-}" = "flash" ]; then
    shift
    [ $# -gt 0 ] || { echo "usage: $0 flash <config>[:<builddir>] ..." >&2; exit 2; }
    for spec in "$@"; do
        c=${spec%%:*}; dir=${spec#*:}; [ "$dir" = "$spec" ] && dir=""
        facts=$(board_facts "$c") || { echo "unknown board config '$c'" >&2; exit 2; }
        read -r serial cable part policy bitname <<<"$facts"
        expected_owner=$(gptp_owner_for_config "$c") || {
            echo "[$c] no gPTP owner contract for this named config" >&2; exit 2; }
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
        # BIOS constants and bind them to the exact parsed bit payload.
        if [ ! -f "$dir/flashboot_layout.json" ] && [ -f "$dir/software/include/generated/soc.h" ]; then
            "${PYTHON:-python3}" "$SOC_DIR/layout_from_soch.py" "$dir" \
                --bit "$dir/gateware/$bitname"
        fi
        case "$policy" in
            boot)
                bit="$dir/gateware/$bitname"
                [ -f "$bit" ] || { echo "[$c] missing $bit" >&2; exit 2; }
                installed_layout="${INSTALLED_LAYOUT:-}"
                installed_bit="${INSTALLED_BIT:-}"
                if [ -z "$installed_layout" ] || [ -z "$installed_bit" ]; then
                    installed_build="${INSTALLED_BUILD:-}"
                    [ -n "$installed_build" ] || {
                        echo "[$c] flash REFUSED: set both INSTALLED_LAYOUT + INSTALLED_BIT, or INSTALLED_BUILD=<exact current build>." >&2
                        exit 2; }
                    case "$installed_build" in
                        /*) ;;
                        *) installed_build="$WORK/$installed_build" ;;
                    esac
                    installed_build=${installed_build%/}
                    installed_layout="$installed_build/flashboot_layout.json"
                    installed_bit="$installed_build/gateware/$bitname"
                fi
                [ -f "$installed_layout" ] || {
                    echo "[$c] missing installed layout $installed_layout" >&2; exit 2; }
                [ -f "$installed_bit" ] || {
                    echo "[$c] missing installed bitstream $installed_bit" >&2; exit 2; }
                echo "== flash-pair [$c] LIVE OWNER-STATE PROOF + ORDERED VERIFIED SET =="
                SERIAL="$serial" CABLE="$cable" FPGA_PART="$part" \
                    LAYOUT="$dir/flashboot_layout.json" \
                    BIT="$bit" \
                    INSTALLED_LAYOUT="$installed_layout" \
                    INSTALLED_BIT="$installed_bit" \
                    EXPECTED_GPTP_OWNER="$expected_owner" \
                    "$SOC_DIR/deploy.sh" flash-pair
                ;;
            images)
                echo "[$c] flash REFUSED: named persistent profiles must carry a complete bitstream+image set for flash-pair." >&2
                exit 2
                ;;
            bitstream)
                echo "[$c] flash REFUSED: named bitstream-only persistent writes cannot preserve an installed owner set." >&2
                exit 2
                ;;
        esac
    done
    exit 0
fi

# ---- named configurations -----------------------------------------------------
cfg_ax7101() {   # shipping bare-metal shape: one cacheless RV32I hart.
                 # cfg_ax8x8 is the 8-stream bare-metal shape and cfg_arty the
                 # Arty bare-metal shape; the Linux profiles and the software
                 # gPTP owner are retired (#259).
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
    # 2026-08-22 (#157): --xlen 32 is STATED. This recipe carried no --xlen
    # from its creation (8a98d265, 07-24) and milan_soc.py defaults to 64, so
    # it implied an RV64 core while the 8x8 config, SOC_DEFAULTS, sweep.sh and
    # the deployed 0x00010022 gateware (x32f1_eto, a sweep build: this recipe
    # has never produced a bitstream) are all RV32 single-hart. An RV64 SoC
    # under the RV32 boot chain hangs at Liftoff with nothing naming the
    # cause (8b5d0255). The 07-24 close above was measured on that RV64 core
    # and its RV64-era refill/prefetch cache profile, so it is an upper bound
    # for this recipe, not its figure.
    # 2026-08-25 (#259): this recipe is BARE-METAL. The retired Linux
    # profile took the L2/scala cache words, the ALSA sound-card and
    # playback rings, and the "full" flash manifest with it; the fabric
    # AAF/TDM datapath and the fabric gPTP owner stay.
    echo "--board ax7101 --cpu vexiiriscv --cpu-count 1 --xlen 32 \
          --software-profile baremetal --all-blocks --coherent-dma --fabric-gptp \
          --milan-clk-freq 100e6 --with-spiflash --flashboot baremetal --gtx-tx-invert \
          --timing-opt --floorplan --eth-port e1 --l2-bytes 0 \
          --uart-baudrate 115200 --rx-queues 2 --strip-probes --hs-page-bytes 16384 \
          --num-streams 8 --audio-interface tdm32 --audio-interface-master \
          --talker-wire-chans 8 --no-latency-taps --no-i2s-playback \
          --entity-gen-dir $SOC_DIR/../../configs/generated/endstation_ax7101_8x8 \
          --no-render-lpf --no-datapath-probes --cbs-queues-mask 0x10 \
          --synth-directive AreaOptimized_high \
          --opt-directive ExploreArea --place-directive AltSpreadLogic_high"
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
                 # eth-port is pinned to e1 (the bench default, same as cfg_ax7101).
                 # If the AX cable is on e2, append `-- --eth-port e2`; AX42's guard
                 # reset scope covers either PHY's tx/gtx path.
}
cfg_arty() {     # Arty A7-100 small endstation: MII 100M, QSPI flashboot (probes stripped since v8 - AVDECC stack needs the slices: v7-style probes overflowed by 181)
    # -1 die: 100 MHz datapath does NOT close (measured -1.0 WNS); 50 MHz is
    # 3.2 Gb/s of 64-bit datapath for a 100 Mbit wire. sys 83.333 = the clean
    # PLL divisor set (VCO 1000; 90e6 has NO solution with the 25 MHz eth ref).
    # Flash = bitstream@0 + the raw AEM image (QSPI self-boot on both boards;
    # the old kernel-at-0 / JTAG-SRAM-only layout and the whole Linux image
    # manifest are retired history - #259 and docs/integration/QSPI_FLASHBOOT.md).
    # 2026-08-22 (#157): --cpu-count 1 --xlen 32 are STATED, matching
    # configs/endstation_arty_current.yaml, the sweep.sh arty leg and
    # configs/generated/sweep_opts_arty.sh. The 2-hart count dated from the
    # launcher's first commit (207192cc) and never matched a deployed Arty
    # bitstream (the m0019 ship was one hart); the absent --xlen implied RV64
    # through milan_soc.py's default. The Arty is a retired DUT
    # (docs/findings/BENCH_TOPOLOGY.md), so this recipe is proven to reach
    # the Instance (test_builder gate 23g), not built.
    # 2026-08-25 (#259): bare-metal, like every named config; the retired
    # Linux profile took the L2/scala cache words and the sound-card with it.
    echo "--board arty --cpu vexiiriscv --cpu-count 1 --xlen 32 \
          --software-profile baremetal --all-blocks --coherent-dma --fabric-gptp \
          --sys-clk-freq 83.333e6 --milan-clk-freq 50e6 --with-spiflash --flashboot baremetal \
          --uart-baudrate 115200 --timing-opt --strip-probes --l2-bytes 0 \
          --cbs-queues-mask 0x10 \
          --entity-gen-dir $SOC_DIR/../../configs/generated/endstation_arty_current \
          --rx-queues 2 --hs-page-bytes 16384"
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
ENTITY_CFG_ax7101="configs/endstation_ax7101_1x1_tdm8.yaml"
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
