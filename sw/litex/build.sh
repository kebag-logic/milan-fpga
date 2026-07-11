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
# Discipline encoded here (docs/findings/SESSION_HANDOFF.md):
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
WORK=/home/alex/litex-milan/work
SOC_DIR="$(cd "$(dirname "$0")" && pwd)"
TAG=${TAG:-$(date +%m%d%H%M)}
STAGGER=90

# ---- per-board flash/JTAG facts (docs/integration/BUILDING.md section 4) --------------------
# serial = FTDI serial (TWO cables on the bus: NEVER omit, a flash op picking the
# wrong board is destructive). policy = what this board's QSPI holds:
#   ax7101 images:    Linux boot images at flashboot_layout.json offsets (kernel at
#                     offset 0) - a bitstream write is the known kernel-clobber trap;
#   arty   images:    the Alinx model since the flashboot port (kernel at offset
#                     0 = mutually exclusive with a bitstream; JTAG-SRAM gateware).
#                     Flash a BITSTREAM instead via: flash arty:<dir> after
#                     flipping this policy - 16 MB cannot hold both.
board_facts() {  # -> "serial cable fpga_part flash_policy bit_name"
    case "$1" in
        ax7101) echo "210512180081 ft232    xc7a100tfgg484 images    alinx_ax7101.bit";;
        arty)   echo "210319AFEED0 digilent xc7a100tcsg324 images    digilent_arty.bit";;
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
            want="flashboot_layout.json"; [ "$policy" = bitstream ] && want="gateware/$bitname"
            dir=$( { ls -td "$WORK"/build_${c}*/ 2>/dev/null || true; } | while read -r d; do
                      [ -f "$d/$want" ] && { echo "$d"; break; }; done || true)
            [ -n "$dir" ] || { echo "[$c] no build containing $want under $WORK/build_${c}* (pass ${c}:<builddir>)" >&2; exit 2; }
        else
            case "$dir" in /*) ;; *) dir="$WORK/$dir";; esac
        fi
        dir=${dir%/}
        case "$policy" in
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
cfg_ax7101() {   # ship shape: cbsf lineage (engine + fold), 2q hs 16K, QSPI flashboot
    echo "--board ax7101 --cpu vexiiriscv --cpu-count 2 --all-blocks --coherent-dma \
          --milan-clk-freq 100e6 --with-spiflash --flashboot full --gtx-tx-invert \
          --timing-opt --floorplan --l2-bytes 65536 \
          --scala-args=--lsu-l1-refill-count=8 --scala-args=--lsu-hardware-prefetch=rpt \
          --scala-args=--l2-down-pending=8 --scala-args=--l2-general-slots=16 \
          --uart-baudrate 115200 --rx-queues 2 --strip-probes --hs-page-bytes 16384 \
          --place-directive ExtraPostPlacementOpt"
}
cfg_arty() {     # Arty A7-100 bring-up: MII 100M, QSPI flashboot (Alinx model), probes KEPT
    # -1 die: 100 MHz datapath does NOT close (measured -1.0 WNS); 50 MHz is
    # 3.2 Gb/s of 64-bit datapath for a 100 Mbit wire. sys 83.333 = the clean
    # PLL divisor set (VCO 1000; 90e6 has NO solution with the 25 MHz eth ref).
    # Flash = LINUX IMAGES at the full-manifest offsets (kernel at 0), so a
    # bitstream in flash is sacrificed - gateware is JTAG-SRAM, like the AX7101.
    echo "--board arty --cpu vexiiriscv --cpu-count 2 --all-blocks --coherent-dma \
          --sys-clk-freq 83.333e6 --milan-clk-freq 50e6 --with-spiflash --flashboot full \
          --uart-baudrate 115200 --timing-opt --l2-bytes 65536 \
          --scala-args=--lsu-l1-refill-count=8 --scala-args=--lsu-hardware-prefetch=rpt \
          --scala-args=--l2-down-pending=8 --scala-args=--l2-general-slots=16 \
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
    cmd="cd $SOC_DIR && source /home/alex/Xilinx2/2026.1/Vivado/settings64.sh && \
         export PATH=/home/alex/litex-milan/venv/bin:\$PATH && \
         exec python3 milan_soc.py $args ${EXTRA[*]:-} --vivado-max-threads 32 --build --output-dir $out"
    if [ "$DRY" = 1 ]; then
        echo "DRY [$name] -> $out"; echo "  $cmd" | tr -s ' '; continue
    fi
    [ "$first" = 1 ] || { echo "stagger ${STAGGER}s (shared pythondata checkout)"; sleep $STAGGER; }
    first=0
    setsid nohup bash -c "$cmd" > "$WORK/build_${name}_${TAG}.launch.log" 2>&1 &
    echo "LAUNCHED [$name] pid=$! out=$out log=$WORK/build_${name}_${TAG}.launch.log"
done
