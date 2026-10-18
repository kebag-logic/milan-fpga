#!/bin/sh
# Build one exported tree's default pp_top binary or the aecp_cmds harness with
# the pinned Verilator and a bounded job count. Usage:
#   build_tree.sh <tree-root> pp_top|aecp_cmds <jobs> <log> <rcfile>
set -u
tree=$1; suite=$2; jobs=$3; log=$4; rcf=$5
V=${VERILATOR_PIN:?set VERILATOR_PIN to the pinned Verilator 5.050 executable}
common="--cc --exe --build -j $jobs -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM"
case $suite in
  pp_top)
    make -C "$tree/tb/pp_top" gsi-build VERILATOR="$V" \
      VFLAGS="$common --top-module pp_top_wrap -CFLAGS \"-std=c++17 -O2 -I$tree/tb/pp_top -Wall -Wextra\"" \
      >"$log" 2>&1
    ;;
  aecp_cmds)
    make -C "$tree/tb/aecp_cmds" build VERILATOR="$V" \
      VFLAGS="$common -Wno-PINCONNECTEMPTY --top-module aecp_cmds_wrap -CFLAGS \"-std=c++17 -O2 -I$tree/tb/aecp_cmds -Wall -Wextra\"" \
      >"$log" 2>&1
    ;;
  *) echo "unknown suite $suite" >"$log"; false ;;
esac
echo $? >"$rcf"
