#!/usr/bin/env bash
# split_place.sh <clone> <elf> <work> - one Vivado PLACEMENT of the split shipping image, a measurement (#665 S6).
#
# The shipping AX7101 argv (build.sh's, as split-firmware.sh takes it) with --ctrl-mailbox --ctrl-firmware <elf>,
# exported (no --build) into <work>/split-1x1; then LiteX's own build script cut after its placement reports, plus a
# post-placement timing summary, so the run is synthesis, opt and placement only. Start it ONLY under the host lock,
# as a background job: setsid nohup flock $VIVADO_LOCK split_place.sh ... > log 2>&1 &
set -euo pipefail
CLONE=$1 ELF=$2 WORK=$3
LITEX=$HOME/litex-milan
VIVADO_SETTINGS=$HOME/Xilinx/2026.1/Vivado/settings64.sh
ARGV="--board ax7101 --milan-clk-freq 50e6 --gtx-tx-invert --floorplan --eth-port e1 --no-i2s-playback --no-render-lpf --num-streams 1 --audio-interface tdm8 --audio-interface-master --audio-interface-render 8 --talker-wire-chans 8 --loopback-lane --fabric-gptp --gptp-ingress-lat-ns 656 --gptp-egress-lat-ns 219 --cpu vexiiriscv --software-profile baremetal --xlen 32 --full --with-spiflash --flashboot baremetal --timing-opt --l2-bytes 0 --uart-baudrate 115200 --cpu-count 1 --synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt"
[ -z "$(git -C "$CLONE" status --porcelain)" ] || { echo "REFUSED: $CLONE is dirty"; exit 1; }
echo "clone $(git -C "$CLONE" rev-parse HEAD) elf $(sha256sum "$ELF" | cut -c1-16) start $(date -u +%FT%TZ)"
OUT=$WORK/split-1x1
[ ! -e "$OUT" ] || mv "$OUT" "$OUT.prev.$(date +%s)"
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LITEX_ENV_CC_TRIPLE=riscv32-linux TMPDIR=$WORK/tmp
export PATH=$HOME/br-milan-rv32/host/bin:$LITEX/venv/bin:$PATH PYTHONPATH=$LITEX/litex:$LITEX/migen
mkdir -p "$TMPDIR"
(cd "$CLONE/sw/litex" && "$LITEX/venv/bin/python3" -B milan_soc.py $ARGV \
   --entity-gen-dir "$CLONE/configs/generated/endstation_ax7101_1x1_tdm8" --vivado-max-threads 8 \
   --ctrl-mailbox --ctrl-firmware "$ELF" --output-dir "$OUT") > "$WORK/split-1x1.export.log" 2>&1
G=$OUT/gateware
cut=$(grep -n '^report_clock_utilization ' "$G/alinx_ax7101.tcl" | cut -d: -f1)
[ -n "$cut" ] || { echo "REFUSED: no placement reports in the build script"; exit 1; }
head -n "$cut" "$G/alinx_ax7101.tcl" > "$G/place_only.tcl"
printf '%s\n' "report_timing_summary -file alinx_ax7101_timing_place.rpt" "exit" >> "$G/place_only.tcl"
grep -q '^route_design' "$G/place_only.tcl" && { echo "REFUSED: the cut script routes"; exit 1; }
source "$VIVADO_SETTINGS"
cd "$G"
rc=0
vivado -mode batch -nojournal -source place_only.tcl > vivado_place.log 2>&1 || rc=$?
echo "vivado rc=$rc end $(date -u +%FT%TZ)"
grep -E "^ERROR|Place 30-487|slices" vivado_place.log | head -20 || true
exit $rc
