#!/bin/sh
# Scratch build of the #530 reproduction against a checkout given as $1
# (default: the lane). Product shape AX7101 1x1 TDM8, the pp_shadow time
# compression, gPTP plane option OFF (the ownerless verification boundary
# the pp_shadow and milan_dp legs use), every signal public for observation.
set -eu
LANE=${1:-$LANES/530-crf-talker-lifecycle}
OBJ=${2:-obj_repro}
V=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$HERE"
SRCS=$(make -s -C "$LANE/tb/verilator/milan_dp" print-srcs | tr ' ' '\n' | sed "s#^\.\./\.\./\.\./#$LANE/#" | tr '\n' ' ')
python3 "$LANE/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py" -o ltn_rom.hex
python3 "$LANE/protocol-processor/hdl/aecp/ucode/gen_ucode.py" -o ucode.hex
# shellcheck disable=SC2086
"$V" --cc --exe --build -j 8 --top-module milan_datapath --Mdir "$OBJ" \
  +incdir+"$LANE/configs/generated/endstation_ax7101_1x1_tdm8" \
  +incdir+"$LANE/hdl/common" +incdir+"$LANE/hdl/common/csr" +incdir+"$LANE/hdl/common/eth_event_counter" \
  +incdir+"$LANE/hdl/ieee17221/adp" +incdir+"$LANE/hdl/ieee8021q/ts" \
  +incdir+"$LANE/hdl/ieee8021as/ptp_timestamp" +incdir+"$LANE/third_party/verilog-axis/rtl" \
  -Wno-fatal -Wno-lint -Wno-style -Wno-TIMESCALEMOD \
  -GCLKV_QTICK_CYC_P=4096 -GLDIAG_IVAL_CYC_P=256 -GDIAG_TICK_CYC_P=256 -GGPTP_PLANE_EN_P=0 \
  -GTALKER_WIRE_CHANS_P=8 -GAUDIO_IF_SLOTS_P=8 -GAUDIO_IF_MASTER_P=1 \
  -GLOOPBACK_P=1 -GI2SPB_P=0 -GLPF_P=0 \
  -GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=100 -GMAAP_CLK_HZ_P=100000 \
  --public-flat-rw \
  -CFLAGS "-std=c++17 -O2" \
  $SRCS "$HERE/sim_repro.cpp" -o Vrepro
