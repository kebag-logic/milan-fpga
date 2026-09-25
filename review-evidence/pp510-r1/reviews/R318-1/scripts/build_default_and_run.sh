#!/bin/sh
# Usage: build_default_and_run.sh <tree>  - default pp_top build only (8 jobs), then run it
set -u
TREE=$1
: "${VERILATOR:?set VERILATOR}"
VF='--cc --exe --build -j 8 --top-module pp_top_wrap -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM'
CF="-std=c++17 -O2 -I$TREE/tb/pp_top -Wall -Wextra"
make -C "$TREE/tb/pp_top" gsi-build VERILATOR="$VERILATOR" VFLAGS="$VF -CFLAGS \"$CF\"" >"$TREE/build.log" 2>&1 || { echo "BUILD FAILED"; tail -30 "$TREE/build.log"; exit 2; }
echo "build ok"
cd "$TREE/tb/pp_top" && ./obj_dir/Vpp_top_sim
echo "exit=$?"
