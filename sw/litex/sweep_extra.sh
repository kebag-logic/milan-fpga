#!/bin/bash
# One-off extra place-directive draws (same BASE as sweep.sh, different
# directives) for when the standard asl/eto/eppo trio misses timing on a
# luck-bound cone. Usage: sweep_extra.sh <arty|ax7101> <tag>
# Seeds: exp=Explore, asm=AltSpreadLogic_medium, enl=ExtraNetDelay_low.
set -euo pipefail
BOARD=${1:?board}; TAG=${2:?tag}
export PATH="$HOME/litex-milan/venv/bin:$PATH"
source /home/alex/Xilinx/2026.1/Vivado/settings64.sh
W=$HOME/litex-milan/work
case "$BOARD" in
  arty)   OPTS="--board arty --sys-clk-freq 83.333e6 --milan-clk-freq 50e6"; L2=65536;;
  ax7101) OPTS="--board ax7101 --milan-clk-freq 100e6 --gtx-tx-invert --floorplan"; L2=32768;;
  *) echo "unknown board $BOARD" >&2; exit 2;;
esac
BASE="python3 $(dirname "$(realpath "$0")")/milan_soc.py $OPTS --cpu vexiiriscv \
 --all-blocks --coherent-dma --with-spiflash --flashboot full --timing-opt \
 --l2-bytes ${L2} --scala-args=--lsu-l1-refill-count=8 \
 --scala-args=--lsu-hardware-prefetch=rpt --scala-args=--l2-down-pending=8 \
 --scala-args=--l2-general-slots=16 --uart-baudrate 115200 --rx-queues 2 \
 --strip-probes --hs-page-bytes 16384 --cpu-count 1 --vivado-max-threads 32 --build"
cd "$W"
rm -rf build_${BOARD}_{exp,asm,enl}_${TAG}
launch() {
  setsid nohup $BASE --place-directive "$2" \
    --output-dir "$W/build_${BOARD}_${1}_${TAG}" \
    > "$W/build_${BOARD}_${1}_${TAG}.launch.log" 2>&1 < /dev/null &
  echo "LAUNCHED [${BOARD}_${1}_${TAG}] pid=$!"
}
launch exp Explore;               sleep 90
launch asm AltSpreadLogic_medium; sleep 90
launch enl ExtraNetDelay_low
