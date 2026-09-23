#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build and run the engine suite of an exported source tree exactly as
# tb/verilator/engine/Makefile does (same flags, same three images), except
# that the Verilator build uses at most 8 jobs instead of "-j 0". Builds in
# a caller-given directory; nothing is written into the exported tree except
# its own suite's ignored image names under the work directory copy.
#
# usage: engine_suite.sh <exported-tree> <work-dir>
# env:   VERILATOR  path of the Verilator wrapper to use (default: verilator)
set -eu
TREE=$(cd "$1" && pwd)
WORK=$2
VERILATOR=${VERILATOR:-verilator}
mkdir -p "$WORK"
WORK=$(cd "$WORK" && pwd)
E="$TREE/tb/verilator/engine"
RTL="$TREE/hdl"
GEN="$RTL/ucode/gen_gptp_ucode.py"
GENARGS="--clk-hz 2000000 --cease-ms 3000"

"$VERILATOR" --version
"$VERILATOR" --cc --exe --build -j 8 --top-module KL_gptp_engine \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
  -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
  -CFLAGS "-std=c++17 -O2 -I$E -Wall -Wextra" \
  --Mdir "$WORK/obj_dir" \
  "$RTL/ucpu/gptp_ucpu_pkg.sv" "$RTL/ucpu/KL_gptp_ucpu.sv" \
  "$RTL/wire/KL_gptp_rx_parser.sv" "$RTL/wire/KL_gptp_tx_slot.sv" \
  "$RTL/common/KL_gptp_timer.sv" "$RTL/top/KL_gptp_engine.sv" \
  "$E/sim_main.cpp" -o Vengine_sim >"$WORK/build.log" 2>&1

rc=0
for img in ship seq sync; do
  mkdir -p "$WORK/run_$img"
  case $img in
    ship) python3 "$GEN" $GENARGS -o "$WORK/run_$img/gptp_ucode.hex" ;;
    seq)  python3 "$GEN" $GENARGS --seq-seed 0x200000 \
            -o "$WORK/run_$img/gptp_ucode.hex" ;;
    sync) python3 "$GEN" $GENARGS --sync-seq-seed 0x10000 \
            -o "$WORK/run_$img/gptp_ucode.hex" ;;
  esac
  set +e
  (cd "$WORK/run_$img" && "$WORK/obj_dir/Vengine_sim") >"$WORK/run_$img.log" 2>&1
  r=$?
  set -e
  echo "image $img: exit $r; $(tail -n 1 "$WORK/run_$img.log")"
  [ $r -eq 0 ] || rc=1
done
exit $rc
