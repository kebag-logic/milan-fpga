#!/bin/bash
# 3-seed Vivado place-directive sweep (bench rule: saturate the box, max 3
# parallel instances at 32 threads). Usage: sweep.sh <arty|ax7101> <tag>
# Bits land in $WORK/build_<board>_{asl,eto,eppo}_<tag>; pick by WNS:
#   grep -A6 "Design Timing Summary" build_*_<tag>/gateware/vivado.log
#
# Shape override (a non-default end-station config for this board):
#   SWEEP_CFG=configs/endstation_arty_4x4.yaml sweep.sh arty 4x4
set -euo pipefail
BOARD=${1:?board}; TAG=${2:?tag}
export PATH="$HOME/litex-milan/venv/bin:$PATH"
source $HOME/Xilinx/2026.1/Vivado/settings64.sh
W=$HOME/litex-milan/work
R="$(cd "$(dirname "$(realpath "$0")")/../.." && pwd)"
# ======================= PER-BOARD DESIGN SHAPE =========================
# SINGLE SOURCE = the end-station configs. These tables are the DEFAULTS;
# sw/builder/endstation_builder.py emits configs/generated/sweep_opts_<board>.sh
# from configs/endstation_*.yaml and it is sourced AFTER them, so anything the
# fragment defines wins and anything it does not define keeps the default (that
# ordering is why a fragment that predates a new knob can never silently drop
# it). Regenerate the fragments with
#   python3 sw/builder/endstation_builder.py configs/endstation_arty_current.yaml
#   python3 sw/builder/endstation_builder.py configs/endstation_ax7101_8x8.yaml
# The builder test gate (test_builder.py gate 9) asserts fragment OPTS/L2/RXQ ==
# these tables byte-for-byte; check_sweep_shape.py asserts the EFFECTIVE
# OPTS/L2/RXQ/NS == the end-station config named in CFG below.
# ========================================================================
case "$BOARD" in
  arty)   OPTS="--board arty --sys-clk-freq 83.333e6 --milan-clk-freq 50e6"; L2=65536; RXQ=2;;
  ax7101) OPTS="--board ax7101 --milan-clk-freq 100e6 --gtx-tx-invert --floorplan --eth-port e1 --no-render-lpf"; L2=16384; RXQ=2;;  # RXQ 1 -> 2 on 2026-07-28 WITH the reflash that re-pins boot_chain_pin (+0x74): the D7 fix - one queue starves ptp4l under RX load and a conformant BMCA deposes our GM. eth-port MUST match the physical cable: the bench cable is on e1 (USER 2026-07-27) and the shipping bitstream was built with the e1 default, so forcing e2 here produced a bitstream that could not reach the network. e2 remains the documented fallback for the 2026-07-22 e1 GMII-RX fault - move the cable FIRST, then change this. L2 16K = the 8x8 shape that closed (build.sh cfg_ax8x8), NOT the 1x1 32K. --no-render-lpf is the SPENT LPF_P area lever (428 LUT / 756 FF, the one Vivado-PROVEN figure of the 07-27 round) on the board that missed placement by 282 slices - the pruned datapath behaves exactly like LPF_CTRL[0]=0 does today, but the analog loop THD+N record was measured THROUGH the filter and must be re-measured before it is quoted against this bitstream
  *) echo "unknown board $BOARD" >&2; exit 2;;
esac
# NS = NxN dataplane width (--num-streams / milan_datapath N_STREAMS). It is a
# SHAPE property, not a board property (arty has both a 1x1 and a 4x4 config),
# which is why it sits on its own line beside the board defaults and beside the
# config it comes from. UNTIL 2026-07-26 sweep.sh passed NO --num-streams AT
# ALL, so `sweep.sh ax7101` built the DEFAULT 1x1 datapath while every config,
# doc and build dir called it 8x8 - the same silent-divergence class as the
# rx-queues bug (5ce9a13), one shape wider.
case "$BOARD" in
  arty)   NS=1; CFG=${SWEEP_CFG:-configs/endstation_arty_current.yaml};;
  ax7101) NS=8; CFG=${SWEEP_CFG:-configs/endstation_ax7101_8x8.yaml};;
esac
GEN_OPTS="$R/configs/generated/sweep_opts_${BOARD}.sh"
if [ -f "$GEN_OPTS" ]; then
  . "$GEN_OPTS"
fi
# A fragment may express the stream count either as `NS=<n>` (preferred: the
# same shape as L2/RXQ) or, historically, inline in OPTS (sweep_opts_arty_4x4.sh
# does). Lift the inline form into NS so there is exactly ONE effective value
# and the gate below sees it; never emit the flag twice (argparse would silently
# keep the last one).
case "$OPTS" in
  *--num-streams*)
    NS="$(printf '%s\n' "$OPTS" | sed -E 's/.*--num-streams[= ]+([0-9]+).*/\1/')"
    ;;
  *)
    if [ "${NS}" -gt 1 ]; then OPTS="$OPTS --num-streams ${NS}"; fi
    ;;
esac
# RXQ is PER BOARD because each board's flashed boot chain fixes its own DMA
# window map (the 2026-07-24 CSR-rot rule): ax7101 ships 1 queue (its csr.csv
# has no rx1_*/steer registers), arty ships 2 (its deployed gateware carries
# rx1_* + steer_q0/q1). Building either with the other's count shifts every
# DMA window under an unchanged DTB - unify them only with a full boot-chain
# rebuild on that board.
#
# HARD GATE (not advisory): the effective shape must equal the end-station
# config this sweep claims to build. set -e turns any disagreement into a
# refusal to launch, so "the config says 8x8, the bitstream is 1x1" cannot
# happen again.
python3 "$R/scripts/check_sweep_shape.py" --board "$BOARD" \
        --config "$CFG" --num-streams "$NS" --rx-queues "$RXQ" --l2-bytes "$L2" \
        --opts "$OPTS"
# SAME GATE, ONE LAYER UP: the gateware `include-s a GENERATED entity
# definition - hdl/common/csr/gen/adp_shape_defaults.svh (the ADPDU stream
# counts served RO at 0x618/0x61C, and the ACMP context-array sizing) and
# hdl/ieee17221/aecp/gen/aecp_aem_rom.svh (the descriptor set a controller
# enumerates). Both are written by the builder FROM A CONFIG, and until
# 2026-07-27 nothing checked that it was THIS config: the tracked ROM was the
# 1x1 shape and every build - including the 8x8 - compiled it in. Refuse to
# launch unless the tree carries the definition of the config being built.
python3 "$R/scripts/check_entity_shape.py" --built-config "$R/$CFG"
BASE="python3 $R/sw/litex/milan_soc.py $OPTS --cpu vexiiriscv \
 --all-blocks --coherent-dma --with-spiflash --flashboot full --timing-opt \
 --l2-bytes ${L2} --scala-args=--lsu-l1-refill-count=8 \
 --scala-args=--lsu-hardware-prefetch=rpt --scala-args=--l2-down-pending=8 \
 --scala-args=--l2-general-slots=16 --uart-baudrate 115200 --rx-queues ${RXQ} \
 --strip-probes --hs-page-bytes 16384 --cpu-count 1 --vivado-max-threads 32 --build"
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
