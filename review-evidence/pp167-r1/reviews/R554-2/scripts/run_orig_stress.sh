#!/usr/bin/env bash
# usage: run_orig_stress.sh VERILATOR TREE_DIR BUILD_DIR CYCLES SEED...
set -euo pipefail
V=$1; T=$2; B=$3; N=$4; shift 4
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$B"
"$V" --cc --exe --build -j 4 --top-module KL_pp_originator \
  -GCA_POOL_P=4 -GPROBE_SLOTS_P=0 -GINFLIGHT_P=4 -GKEY_W_P=16 \
  -Wno-fatal -Wno-lint -Wno-style --Mdir "$B" -CFLAGS "-std=c++17 -O2" \
  "$T/hdl/common/pp_pkg.sv" "$T/hdl/packet_engine/KL_pp_originator.sv" \
  "$HERE/probe_orig_cancel_fail.cpp" -o Vstress >"$B/build.log" 2>&1
rc=0
for s in "$@"; do echo "seed $s"; "$B/Vstress" "$N" "$s" || rc=1; done
exit $rc
