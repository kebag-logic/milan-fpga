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
# Discipline encoded here (docs/SESSION_HANDOFF.md):
#   * every build: setsid nohup (harness task-kills must never reap Vivado),
#     --vivado-max-threads 32 (Vivado hard cap), launch log next to the outdir;
#   * parallel launches staggered 90 s (shared pythondata git checkout: two
#     concurrent LiteX elaborations race on index.lock and crash);
#   * at most 3 concurrent builds (3 x 32 = the 96-core box saturated).
#
# Configs are FUNCTIONS below - one place to edit a board's canonical shape.
# MAINTAINER DOC: docs/BUILDING.md (configs, discipline rationale, per-board
# load/console facts, gates). Update it when adding a config or a rule here.

set -euo pipefail
WORK=/home/alex/litex-milan/work
SOC_DIR="$(cd "$(dirname "$0")" && pwd)"
TAG=${TAG:-$(date +%m%d%H%M)}
STAGGER=90

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
cfg_arty() {     # Arty A7-100 bring-up: MII 100M, serial boot, probes KEPT
    echo "--board arty --cpu vexiiriscv --cpu-count 2 --all-blocks --coherent-dma \
          --milan-clk-freq 100e6 --timing-opt --l2-bytes 65536 \
          --scala-args=--lsu-l1-refill-count=8 --scala-args=--lsu-hardware-prefetch=rpt \
          --scala-args=--l2-down-pending=8 --scala-args=--l2-general-slots=16 \
          --uart-baudrate 115200 --rx-queues 2 --hs-page-bytes 16384"
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
