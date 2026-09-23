#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# The two other suites whose tracked ROM images this PR changes, `run`
# targets only (no mutation arms), pinned Verilator, at most 8 build jobs.
set -u
. "$(dirname "$0")/env.sh"
dir=$SCRATCH/rom-suites-head
rm -rf "$dir"; mkdir -p "$dir"
git -C "$CLONE" archive "$HEAD_SHA" | tar -x -C "$dir"
rc=0
for s in tb/verilator/ucpu tb/tsngen; do
  echo "== $s (image sha256 $(sha256sum "$dir/$s/gptp_ucode.hex" | cut -d' ' -f1))"
  flags="--cc --exe --build -j 8 -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -GUCODE_HEX_P='\"gptp_ucode.hex\"'"
  case $s in
    tb/verilator/ucpu) flags="$flags --top-module KL_gptp_ucpu";;
    tb/tsngen) flags="$flags --top-module KL_gptp_engine -GCLK_HZ_P=2000000";;
  esac
  make -C "$dir/$s" run VERILATOR="$PINNED_VERILATOR" \
    VFLAGS="$flags -CFLAGS \"-std=c++17 -O2 -Wall -Wextra -I$dir/$s\"" 2>&1 \
    | grep -vE '^(g\+\+|python3 .*verilator_includer|make\[|rm |- V|- Verilator)' || rc=1
  [ -f "$dir/$s/obj_dir/Vucpu_sim" ] || [ -f "$dir/$s/obj_dir/Vtsngen" ] || rc=1
done
exit $rc
