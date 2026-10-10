#!/bin/sh
# Reviewer probe: open-tool primitive mapping (Yosys synth_xilinx, 7-series)
# of the changed tables, base against head, module by module.
# Usage: yosys_map.sh <repo> <workdir>   (needs git, sv2v, yosys)
set -eu
REPO=$1
W=$2
BASE=e8454e2751d05b02ee8e5a571857589ab358ab86
GP_BASE=5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d
mkdir -p "$W"
cd "$W"
git -C "$REPO" show "$BASE:hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv" > txret_base.sv
cp "$REPO/hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv" txret_head.sv
git -C "$REPO/gptp-processor" show "$GP_BASE:hdl/common/KL_gptp_timer.sv" > timer_base.sv
cp "$REPO/gptp-processor/hdl/common/KL_gptp_timer.sv" timer_head.sv
AXIS="$REPO/third_party/verilog-axis/rtl/axis_fifo.v"
syn() {  # name top files... -- yosys chparam args
  name=$1; top=$2; shift 2
  files=""
  while [ "$1" != "--" ]; do files="$files $1"; shift; done
  shift
  sv2v -DSYNTHESIS $files > "$name.v"
  yosys -q -p "read_verilog -DSYNTHESIS $name.v; chparam $* $top; synth_xilinx -family xc7 -top $top -flatten; tee -o $name.stat stat" > "$name.ylog" 2>&1
  printf '%s:' "$name"
  grep -E '^ +[0-9]+ +(RAM32M|RAM32X1D|RAM64M|RAM64X1D|RAMB18E1|RAMB36E1|FDRE|FDSE|FDCE|FDPE|LUT[1-6]|MUXF7|MUXF8)$' "$name.stat" \
    | awk '{printf " %s=%s", $2, $1}'
  echo
}
syn txret_base KL_gptp_txret txret_base.sv -- -set TXTS_CAP_N_P 8
syn txret_head KL_gptp_txret txret_head.sv -- -set TXTS_CAP_N_P 8
syn timer_base KL_gptp_timer timer_base.sv -- -set SLOTS_P 8
syn timer_head KL_gptp_timer timer_head.sv -- -set SLOTS_P 8
# the frame FIFO storage: old 64 data + 8 keep + last (+ 1 user on RX),
# new 64 data + last + 4 user, 256 beats either way
syn rxfifo_base axis_fifo "$AXIS" -- -set DEPTH 2048 -set DATA_WIDTH 64 -set KEEP_ENABLE 1 -set KEEP_WIDTH 8 -set USER_ENABLE 1 -set USER_WIDTH 1 -set ID_ENABLE 0 -set DEST_ENABLE 0 -set FRAME_FIFO 1 -set DROP_BAD_FRAME 1 -set DROP_OVERSIZE_FRAME 1 -set DROP_WHEN_FULL 1
syn rxfifo_head axis_fifo "$AXIS" -- -set DEPTH 256 -set DATA_WIDTH 64 -set KEEP_ENABLE 0 -set KEEP_WIDTH 8 -set USER_ENABLE 1 -set USER_WIDTH 4 -set USER_BAD_FRAME_VALUE 1 -set USER_BAD_FRAME_MASK 1 -set ID_ENABLE 0 -set DEST_ENABLE 0 -set FRAME_FIFO 1 -set DROP_BAD_FRAME 1 -set DROP_OVERSIZE_FRAME 1 -set DROP_WHEN_FULL 1
syn txfifo_base axis_fifo "$AXIS" -- -set DEPTH 2048 -set DATA_WIDTH 64 -set KEEP_ENABLE 1 -set KEEP_WIDTH 8 -set USER_ENABLE 0 -set ID_ENABLE 0 -set DEST_ENABLE 0 -set FRAME_FIFO 1
syn txfifo_head axis_fifo "$AXIS" -- -set DEPTH 256 -set DATA_WIDTH 64 -set KEEP_ENABLE 0 -set KEEP_WIDTH 8 -set USER_ENABLE 1 -set USER_WIDTH 4 -set ID_ENABLE 0 -set DEST_ENABLE 0 -set FRAME_FIFO 1
