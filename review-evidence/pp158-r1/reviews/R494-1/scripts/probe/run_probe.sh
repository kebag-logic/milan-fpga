#!/bin/sh
# Usage: run_probe.sh TREE OUTLOG VERILATOR  (TREE = extraction holding hdl/ and tb/common/)
set -u
T=$1 LOG=$2 V=$3; D=$(dirname "$0")
mkdir -p "$T/tb/r494_probe"; cp "$D/probe_main.cpp" "$T/tb/r494_probe/"
cd "$T/tb/r494_probe" && "$V" --cc --exe --build -j 0 --top-module KL_aecp_notify \
  -GN_CTRL_P=3 -GN_STREAM_IN_P=1 -GN_STREAM_OUT_P=1 -Wno-fatal -Wno-lint -Wno-style \
  -CFLAGS "-std=c++17 -O2" ../../hdl/common/pp_pkg.sv ../../hdl/aecp/KL_aecp_notify.sv probe_main.cpp -o Vprobe > build.log 2>&1 \
  && ./obj_dir/Vprobe > "$LOG" 2>&1; echo $? > "$LOG.rc"
