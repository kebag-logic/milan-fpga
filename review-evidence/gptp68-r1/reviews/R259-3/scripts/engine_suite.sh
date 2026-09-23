#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# engine_suite.sh REV DIR: export REV from the clone into $SCRATCH/DIR and run
# the engine suite's `run` target (shipping + both seeded images) with the
# pinned Verilator, at most 8 build jobs. The clone is never written.
set -eu
. "$(dirname "$0")/env.sh"
rev=$1; dir=$SCRATCH/$2
rm -rf "$dir"; mkdir -p "$dir"
git -C "$CLONE" archive "$rev" | tar -x -C "$dir"
echo "exported $(git -C "$CLONE" rev-parse "$rev") to scratch/$2"
cd "$dir/tb/verilator/engine"
sha256sum gptp_ucode.hex
make run VERILATOR="$PINNED_VERILATOR" \
  VFLAGS="--cc --exe --build -j 8 --top-module KL_gptp_engine -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -GUCODE_HEX_P='\"gptp_ucode.hex\"' -GCLK_HZ_P=2000000 -CFLAGS \"-std=c++17 -O2 -I$dir/tb/verilator/engine -Wall -Wextra\""
