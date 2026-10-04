#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# oor/run.sh OUT_DIR: build and run the out-of-range packed-read check with
# the `verilator` first on PATH (the pinned 5.050), as the walk arms build.
set -eu
H=$(cd "$(dirname "$0")" && pwd); O=$1; mkdir -p "$O"; cd "$O"
verilator --cc --exe --build -j 4 --x-initial unique -Wno-fatal -Wno-lint --top-module oor \
  "$H/oor.sv" "$H/oor_main.cpp" -o Voor > build.log 2>&1
./obj_dir/Voor +verilator+rand+reset+2
