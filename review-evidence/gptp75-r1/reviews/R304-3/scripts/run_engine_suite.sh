#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R304-3: run the shipped engine suite (three images) from an exported tree,
# with the Verilator build capped at 8 jobs instead of the Makefile's -j 0.
# usage: run_engine_suite.sh EXPORTED_TREE   (pinned verilator first on PATH)
set -eu
T=$1
cd "$T/tb/verilator/engine"
exec make run VFLAGS="--cc --exe --build -j 8 --top-module KL_gptp_engine \
 -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
 -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -GUCODE_HEX_P='\"gptp_ucode.hex\"' \
 -GCLK_HZ_P=2000000 -CFLAGS \"-std=c++17 -O2 -I$(pwd) -Wall -Wextra\""
