#!/bin/sh
# Usage: run_pp_top.sh <tree> [make-target]
# Runs tb/pp_top in <tree> with the pinned Verilator, capping the C++ build
# at 8 jobs (the Makefile's own VFLAGS use -j 0). Exit status is make's.
set -u
TREE=$1; TGT=${2:-run}
: "${VERILATOR:?set VERILATOR to the pinned 5.050 binary}"
VF='--cc --exe --build -j 8 --top-module pp_top_wrap -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM'
CF="-std=c++17 -O2 -I$TREE/tb/pp_top -Wall -Wextra"
"$VERILATOR" --version
exec make -C "$TREE/tb/pp_top" "$TGT" VERILATOR="$VERILATOR" VFLAGS="$VF -CFLAGS \"$CF\""
