#!/usr/bin/env bash
# Build and run the R458-4 lockstep at one shape.
# Usage: run_lockstep.sh <head checkout> <base checkout> <work dir> <M> <N> <cycles> <seeds...>
# verilator (the pinned 5.050) on PATH. Exit 0 = every run 0 mismatches.
set -u
here=$(cd "$(dirname "$0")" && pwd)
head=$1 base=$2 work=$3 m=$4 n=$5 cyc=$6; shift 6
mkdir -p "$work"
python3 "$here/gen_lockstep.py" "$head" "$base" "$work/gen" || exit 2
verilator --cc --exe --build -j 2 --top-module ls_top -Wno-fatal -Wno-WIDTH -Wno-lint \
  --x-initial unique -GN_SOURCES_P="$m" -GN_SINKS_P="$n" \
  -CFLAGS "-std=c++17 -O2 -DTB_M=$m -DTB_N=$n" --Mdir "$work/obj_${m}x${n}" \
  "$head/hdl/common/pp_pkg.sv" "$head/hdl/srp/srp_pkg.sv" \
  "$head/hdl/srp/KL_srp_talker_fsm.sv" "$head/hdl/srp/KL_srp_listener_fsm.sv" \
  "$head/hdl/srp/KL_srp_admission.sv" "$work"/gen/base/*.sv "$work/gen/ls_top.sv" \
  "$here/ls_main.cpp" -o Vls > "$work/build_${m}x${n}.log" 2>&1 || { echo "BUILD FAILED ${m}x${n}"; tail -20 "$work/build_${m}x${n}.log"; exit 2; }
rc=0
for s in "$@"; do
  "$work/obj_${m}x${n}/Vls" "$s" "$cyc" +verilator+rand+reset+2 +verilator+seed+"$s" || rc=1
done
exit $rc
