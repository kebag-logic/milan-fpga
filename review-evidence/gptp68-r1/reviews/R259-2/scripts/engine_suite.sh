#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build and run the engine suite (shipping image, then both seeded images)
# on a fresh export of the head, with the pinned Verilator, capped at 8
# build jobs.
set -eu
. "$(dirname "$0")/env.sh"
tree="$SCRATCH/engine_tree"
rm -rf "$tree"; mkdir -p "$tree"
git -C "$CLONE" archive "$HEAD_SHA" | tar -x -C "$tree"
echo "# verilator: $(verilator --version); head $HEAD_SHA"
cd "$tree/tb/verilator/engine"
make clean >/dev/null
make run VFLAGS="--cc --exe --build -j 8 --top-module KL_gptp_engine -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -GUCODE_HEX_P='\"gptp_ucode.hex\"' -GCLK_HZ_P=2000000 -CFLAGS \"-std=c++17 -O2 -I$tree/tb/verilator/engine -Wall -Wextra\""
