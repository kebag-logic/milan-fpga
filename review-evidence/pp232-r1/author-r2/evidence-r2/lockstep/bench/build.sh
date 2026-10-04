#!/usr/bin/env bash
# usage: build.sh <candidate.sv> <objdir> <busy-signal> [verilator -G args...]
set -euo pipefail
cand=$1; obj=$2; busy=$3; shift 3
here=$(cd "$(dirname "$0")" && pwd)
hdl=$SCRATCH/r1b/tree-head/hdl
export PATH=$PINNED_VERILATOR:$PATH
python3 "$here/gen_wrap.py" "$here/ref/KL_aecp_notify.sv" "$here/$obj.wrap.sv" "$here/outputs.txt"
sed -i "s/IXBUSY/$busy/" "$here/$obj.wrap.sv"
cp "$here/$obj.wrap.sv" "$here/lockstep_top_$obj.sv"
verilator --cc --exe --build -j 4 --top-module lockstep_top -Wno-fatal -Wno-WIDTH -Wno-UNUSED \
  -Wno-DECLFILENAME -Wno-MULTIDRIVEN "$@" --Mdir "$here/$obj" \
  "$hdl/common/pp_pkg.sv" "$here/ref/KL_aecp_notify_ref.sv" "$cand" "$here/lockstep_top_$obj.sv" \
  "$here/tb_lockstep.cpp" -o Vls -CFLAGS "-O2" > "$here/$obj.build.log" 2>&1
echo built "$here/$obj/Vls"
