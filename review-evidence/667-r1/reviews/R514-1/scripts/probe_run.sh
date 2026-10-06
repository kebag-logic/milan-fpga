#!/usr/bin/env bash
# Build and run the reviewer startup probe against one packetizer source.
# usage: probe_run.sh RTL PCH NT MDIR [STALL_MODE]
set -u
here="$(cd "$(dirname "$0")" && pwd)"
rtl="$1"; pch="$2"; nt="$3"; mdir="$4"; stall="${5:-0}"
V="${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}"
"$V" --cc --exe --build -j "${VERILATOR_JOBS:-2}" --top-module KL_aaf_packetizer \
  -GN_TALKERS_P="$nt" -GWIRE_CHANS_P=$((2 * pch)) --Mdir "$mdir" -Wall -Wno-fatal \
  -CFLAGS "-std=c++17 -O2 -DPCH=$pch -DNT=$nt" "$rtl" "$here/probe_start.cpp" \
  > "$mdir.build.log" 2>&1 || { echo "BUILD FAILED rc=$?"; tail -30 "$mdir.build.log"; exit 2; }
sha256sum "$rtl"
"$mdir/VKL_aaf_packetizer" "$stall"
