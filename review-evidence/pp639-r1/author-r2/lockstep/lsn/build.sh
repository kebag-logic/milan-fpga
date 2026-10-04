#!/bin/sh
# build.sh <candidate listener.sv> <N_SINKS_P> <objdir>
set -e
B=$VALIDATION_STORAGE/pp639-a525/base/hdl
verilator --cc --exe --build -j 4 -Wno-fatal -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDSIGNAL \
  -Wno-UNUSEDPARAM -Wno-DECLFILENAME -GN_SINKS_P=$2 --top-module tb_lsn --Mdir "$3" -CFLAGS "-O2" \
  $B/common/pp_pkg.sv $B/acmp/pp_acmp_pkg.sv ref_listener.sv "$1" tb_lsn.sv sim.cpp -o sim > "$3.build.log" 2>&1
