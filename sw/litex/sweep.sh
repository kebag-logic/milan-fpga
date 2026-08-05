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
# The CPU netlist must be the SAME netlist for every seed, or the sweep is not
# measuring the place directive. LiteX builds the VexiiRiscv argument string
# from a python SET (litex/soc/cores/cpu/vexiiriscv/core.py: `",".join(isa_map)`),
# so without a fixed hash seed the --with-isa order is different in every
# process, the netlist-cache key is different, and SpinalHDL regenerates the
# core. MEASURED 2026-08-02 across six otherwise-identical ax7101 builds: the
# regenerated cores placed at 12122, 12130, 12150, 12178, 12179 and 12661 LUTs
# - a 539-LUT spread, on a design that fills 89% of the part, attached to
# nothing anyone changed. That is larger than most RTL levers this campaign
# spends a build on, and it lands as unexplained WNS noise between seeds.
export PYTHONHASHSEED=0
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
  arty)   OPTS="--board arty --sys-clk-freq 83.333e6 --milan-clk-freq 50e6 --num-streams 4 --audio-interface tdm8 --audio-interface-master --talker-wire-chans 4 --cbs-queues-mask 0x10"; L2=16384; RXQ=2;;  # L2 16K since 2026-07-29 (USER; uniform with the AX). 4x4 tdm8-MASTER is the shipping Arty shape since 2026-07-28 (the 8.3b decision: TDM8 physical capture + the I2S Pmod blended as pair slot 0); arty_current (1x1 i2s) remains for build.sh recipes and history
  ax7101) OPTS="--board ax7101 --milan-clk-freq 100e6 --gtx-tx-invert --floorplan --eth-port e1 --no-i2s-playback --no-render-lpf --audio-interface tdm8 --audio-interface-master --talker-wire-chans 8 --cbs-queues-mask 0x10 --loopback-lane --aaf-playback --aaf-playback-streams 1"; L2=16384; RXQ=2;;  # USER 2026-08-05: the SHIPPING AX shape is 1x1x8 TDM8 (endstation_ax7101_1x1_tdm8.yaml) - one 8ch talker + one 8ch listener with the loopback lane BACKED (4 pair holds; the 8x8 refused it at +2303 LUT), latency taps + datapath probes back on (1x1 headroom). The inline table states the shipping design IN FULL because it is the fallback when the fragment is missing - the 2026-07-28 lesson (three seeds built a default-I2S 2ch datapath while every artifact said tdm32 8ch) applies to every shape change. The 8x8 NxN shape remains one SWEEP_CFG=configs/endstation_ax7101_8x8.yaml away; its flags live in that config, not here. RXQ 2 = the D7 gPTP-starvation fix; eth-port e1 = the cabled port (USER 2026-07-27).
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
  arty)   NS=4; CFG=${SWEEP_CFG:-configs/endstation_arty_4x4.yaml};;
  ax7101) NS=1; CFG=${SWEEP_CFG:-configs/endstation_ax7101_1x1_tdm8.yaml};;  # USER 2026-08-05: 1x1x8 TDM8 is the shipping AX shape for now; the fragment's NS=1 overrides the inline 8 (SWEEP_CFG=configs/endstation_ax7101_8x8.yaml returns to the NxN shape)
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
# PER-CONFIG entity definition (USER 2026-07-28: both boards concurrently):
# regenerate THIS config's generated/ copy right here and point the build at
# it with --entity-gen-dir. The tracked hdl/ svh stops being a sweep concern
# entirely - no ownership handoff, no serialization between boards - and the
# freshness "gate" is construction: the builder ran in THIS shell one line
# above, on the same CFG the sweep builds. check_entity_shape still proves
# the per-config copy agrees with the config end to end.
python3 "$R/sw/builder/endstation_builder.py" "$R/$CFG" > /dev/null
CFG_GEN="$R/configs/generated/$(basename "$CFG" .yaml)"
[ -f "$CFG_GEN/gen/adp_shape_defaults.svh" ] || { echo "sweep: $CFG_GEN missing the generated entity definition"; exit 1; }
# The old tracked-svh ownership gate is retired FOR SWEEPS: the build no
# longer reads the tracked copy at all (--entity-gen-dir above), so checking
# it would re-serialize the boards for a file the build ignores. What must
# hold instead: the per-config copy the build DOES read names this config.
grep -q "$(basename "$CFG")" "$CFG_GEN/gen/adp_shape_defaults.svh" || {
  echo "sweep: $CFG_GEN/gen/adp_shape_defaults.svh does not name $(basename "$CFG") as its source"; exit 1; }
# Flow directives are part of the REFERENCE recipe since 2026-07-28: the
# 0x0019 fabric only packs the xc7a100t with opt_design ExploreArea (measured
# -530/-621 slices of packing demand per board) on top of AreaOptimized_high
# synthesis; the 07-24 note that rejected AreaOptimized was about timing at
# the old margin (pre multicycle-reset, pre CBS-mask). The 3-seed WNS pick
# stays the timing guard.
BASE="python3 $R/sw/litex/milan_soc.py $OPTS --cpu vexiiriscv \
 --entity-gen-dir $CFG_GEN \
 --synth-directive AreaOptimized_high --opt-directive ExploreArea \
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
