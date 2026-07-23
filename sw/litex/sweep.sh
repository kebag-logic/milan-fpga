#!/bin/bash
# 3-seed Vivado place-directive sweep (bench rule: saturate the box, max 3
# parallel instances at 32 threads). Usage: sweep.sh <arty|ax7101> <tag>
# Bits land in $WORK/build_<board>_{asl,eto,eppo}_<tag>; pick by WNS:
#   grep -A6 "Design Timing Summary" build_*_<tag>/gateware/vivado.log
set -euo pipefail
BOARD=${1:?board}; TAG=${2:?tag}
export PATH="$HOME/litex-milan/venv/bin:$PATH"
source /home/alex/Xilinx/2026.1/Vivado/settings64.sh
W=$HOME/litex-milan/work
# Per-board design OPTS/L2: SINGLE SOURCE = the end-station configs.
# sw/builder/endstation_builder.py emits configs/generated/sweep_opts_<board>.sh
# from configs/endstation_*.yaml; sourced when present.
GEN_OPTS="$(dirname "$(realpath "$0")")/../../configs/generated/sweep_opts_${BOARD}.sh"
if [ -f "$GEN_OPTS" ]; then
  . "$GEN_OPTS"
else
  # ============================ FALLBACK ONLY ============================
  # No generated fragment found - these inline tables are the FALLBACK, not
  # the source of truth. Regenerate the fragments with
  #   python3 sw/builder/endstation_builder.py configs/endstation_arty_current.yaml
  #   python3 sw/builder/endstation_builder.py configs/endstation_ax7101_8x8.yaml
  # The builder test gate asserts fragment == these tables byte-for-byte.
  # =======================================================================
  case "$BOARD" in
    arty)   OPTS="--board arty --sys-clk-freq 83.333e6 --milan-clk-freq 50e6"; L2=65536;;
    ax7101) OPTS="--board ax7101 --milan-clk-freq 100e6 --gtx-tx-invert --floorplan --eth-port e2"; L2=32768;;  # e2 since 2026-07-22 (e1 GMII-RX hardware fault, cold-soak-proven)
    *) echo "unknown board $BOARD" >&2; exit 2;;
  esac
fi
BASE="python3 $(dirname "$(realpath "$0")")/milan_soc.py $OPTS --cpu vexiiriscv \
 --all-blocks --coherent-dma --with-spiflash --flashboot full --timing-opt \
 --l2-bytes ${L2} --scala-args=--lsu-l1-refill-count=8 \
 --scala-args=--lsu-hardware-prefetch=rpt --scala-args=--l2-down-pending=8 \
 --scala-args=--l2-general-slots=16 --uart-baudrate 115200 --rx-queues 2 \
 --strip-probes --hs-page-bytes 16384 --cpu-count 1 --vivado-max-threads 32 \
 --update-repo no --build"
cd "$W"
rm -rf build_${BOARD}_{asl,eto,eppo}_${TAG}
launch() {
  setsid nohup $BASE --place-directive "$2" \
    --output-dir "$W/build_${BOARD}_${1}_${TAG}" \
    > "$W/build_${BOARD}_${1}_${TAG}.launch.log" 2>&1 < /dev/null &
  echo "LAUNCHED [${BOARD}_${1}_${TAG}] pid=$!"
}
launch asl AltSpreadLogic_high;  sleep 90
launch eto ExtraTimingOpt;       sleep 90
launch eppo ExtraPostPlacementOpt
