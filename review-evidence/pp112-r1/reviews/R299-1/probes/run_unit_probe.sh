#!/bin/sh
# Usage: run_unit_probe.sh <tree-root> <head|base> <N> <out-dir>
# Builds the cross-source probe against <tree-root>/hdl/srp/KL_srp_admission.sv.
# head: the suite's wrapper (invalidate_i connected); base: probes/base_admission_wrap.sv.
set -eu
TREE=$1; KIND=$2; N=$3; OUT=$4
HERE=$(cd "$(dirname "$0")" && pwd)
VERILATOR=${VERILATOR:-verilator}
if [ "$KIND" = head ]; then WRAP=$TREE/tb/srp_admission/srp_admission_wrap.sv
else WRAP=$HERE/base_admission_wrap.sv; fi
mkdir -p "$OUT"
"$VERILATOR" --cc --exe --build -j 4 --top-module srp_admission_wrap \
  -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
  -GN_SOURCES_P="$N" --Mdir "$OUT/obj" \
  -CFLAGS "-std=c++17 -O2 -DTB_SOURCES=$N -DVTOP=Vsrp_admission_wrap -DVTOP_H='\"Vsrp_admission_wrap.h\"'" \
  "$TREE/hdl/srp/KL_srp_admission.sv" "$WRAP" "$HERE/cross_source_probe.cpp" \
  -o probe >/dev/null
"$OUT/obj/probe"
