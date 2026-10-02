#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build probe_meter.cpp against an exported head tree's meter_wrap.sv and RTL.
# Usage: probe_meter.sh <tree> <objdir>   (VERILATOR may name the pinned binary)
set -eu
T=$(cd "$1" && pwd); O=$2; HERE=$(cd "$(dirname "$0")" && pwd)
V=${VERILATOR:-verilator}
"$V" --cc --exe --build -j 8 --top-module meter_wrap -GCLK_HZ_P=200000 \
  -Wno-fatal -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDSIGNAL -Wno-PINCONNECTEMPTY \
  -CFLAGS "-std=c++17 -O2 -DCLK_HZ_TB=200000" -Mdir "$O" \
  "$T/hdl/ieee1722/avtp/avtp_subtype_pkg.sv" "$T/hdl/ieee1722/crf/KL_aaf_clock_meter.sv" \
  "$T/hdl/ieee1722/crf/KL_crf_rx.sv" "$T/tb/verilator/aaf_clock_meter/meter_wrap.sv" \
  "$HERE/probe_meter.cpp" -o Vprobe >/dev/null
exec "$O/Vprobe"
