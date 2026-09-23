#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Run the parent's tb/verilator/gptp_plane suite (files fetched at parent live
# dev and checked against their blob ids by the caller) against one exported
# donor tree placed at gptp-processor/, in a disposable copy. Same flags as
# the parent Makefile except "-j 8" for the Verilator build.
#
# usage: parent_gptp_plane.sh <parent-files-dir> <donor-tree> <work-dir>
# env:   VERILATOR  path of the Verilator wrapper to use (default: verilator)
set -eu
PF=$(cd "$1" && pwd)
DONOR=$(cd "$2" && pwd)
WORK=$3
VERILATOR=${VERILATOR:-verilator}
rm -rf "$WORK"
mkdir -p "$WORK"
cp -a "$PF/tb" "$PF/hdl" "$WORK/"
cp -a "$DONOR" "$WORK/gptp-processor"
cd "$WORK/tb/verilator/gptp_plane"
python3 ../../../gptp-processor/hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 \
  -o gptp_ucode.hex
"$VERILATOR" --cc --exe --build -j 8 --top-module gptp_plane_wrap \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
  -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
  -CFLAGS "-std=c++17 -O2 -I$(pwd) -Wall -Wextra" \
  gptp_plane_wrap.sv \
  ../../../hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv \
  ../../../gptp-processor/hdl/ucpu/gptp_ucpu_pkg.sv \
  ../../../gptp-processor/hdl/ucpu/KL_gptp_ucpu.sv \
  ../../../gptp-processor/hdl/wire/KL_gptp_rx_parser.sv \
  ../../../gptp-processor/hdl/wire/KL_gptp_tx_slot.sv \
  ../../../gptp-processor/hdl/common/KL_gptp_timer.sv \
  ../../../gptp-processor/hdl/top/KL_gptp_engine.sv \
  sim_main.cpp -o Vgptp_plane_sim >build.log 2>&1
set +e
./obj_dir/Vgptp_plane_sim >run.log 2>&1
r=$?
set -e
echo "exit $r; $(tail -n 1 run.log)"
grep -E '^FAIL' run.log | cut -c1-120 || true
