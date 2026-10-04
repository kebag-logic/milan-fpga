#!/bin/sh
# build.sh <dut.sv> <TMR_AW_C> <objdir>
set -e
PKG=$VALIDATION_STORAGE/pp639-a525/base/hdl/common/pp_pkg.sv
verilator --cc --exe --build -j 4 -Wno-fatal -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDSIGNAL \
  -GTMR_AW_C=$2 --top-module tb_top --Mdir "$3" -CFLAGS "-O2" \
  $PKG ref.sv "$1" tb_top.sv sim.cpp -o sim > "$3.build.log" 2>&1
