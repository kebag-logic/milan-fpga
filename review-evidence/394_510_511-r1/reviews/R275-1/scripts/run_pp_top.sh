#!/usr/bin/env bash
# Build and run protocol-processor tb/pp_top in an exported tree with the
# scoped Verilator 5.050, capped at 8 build jobs (the Makefile's -j 0 is
# overridden; every other flag is the Makefile's own).
# Usage: run_pp_top.sh <pp-tree> <verilator-wrapper>
set -u
tree=$1; vl=$2
cd "$tree/tb/pp_top" || exit 2
vflags='--cc --exe --build -j 8 --top-module pp_top_wrap -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM'
make -j1 run VERILATOR="$vl" VFLAGS="$vflags -CFLAGS \"-std=c++17 -O2 -I$PWD -Wall -Wextra\"" MAKEFLAGS=
