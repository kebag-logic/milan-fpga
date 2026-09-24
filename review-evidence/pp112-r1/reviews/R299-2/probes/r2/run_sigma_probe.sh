#!/bin/sh
# Usage: run_sigma_probe.sh <tree-root> <N> <out-dir> <single|multi> [seeds]
# Builds sigma_random_probe.cpp against <tree-root>/hdl/srp/KL_srp_admission.sv
# and the suite's capture wrapper <tree-root>/tb/srp_admission/srp_admission_wrap.sv.
set -eu
TREE=$1; N=$2; OUT=$3; MODE=$4; SEEDS=${5:-200}
HERE=$(cd "$(dirname "$0")" && pwd)
VERILATOR=${VERILATOR:-verilator}
mkdir -p "$OUT"
"$VERILATOR" --cc --exe --build -j 4 --top-module srp_admission_wrap \
  -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
  -GN_SOURCES_P="$N" --Mdir "$OUT/obj" \
  -CFLAGS "-std=c++17 -O2 -DTB_SOURCES=$N -DVTOP=Vsrp_admission_wrap -DVTOP_H='\"Vsrp_admission_wrap.h\"'" \
  "$TREE/hdl/srp/KL_srp_admission.sv" "$TREE/tb/srp_admission/srp_admission_wrap.sv" \
  "$HERE/sigma_random_probe.cpp" -o probe >/dev/null
"$OUT/obj/probe" "$MODE" "$SEEDS"
