#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build one base-versus-head lockstep at one shape and run it over seeds.
# usage: build_run.sh <head-hdl> <base-hdl> <module> <count-param> <N> <work> <cycles> <seed>...
# VERILATOR names the simulator; LS_CFLAGS=-DLS_ANY_INDEX also drives out-of-range
# indices on a valid gate or control op (outside KL_srp_top's contract). Exit 0 only if every seed shows 0 mismatches.
set -eu
HEAD=$1 BASE=$2 MOD=$3 NP=$4 N=$5 WORK=$6 CYC=$7
shift 7
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$WORK"
sed -e "s/\bmodule $MOD\b/module B_$MOD/" -e "s/endmodule : $MOD\b/endmodule : B_$MOD/" \
  "$BASE/srp/$MOD.sv" > "$WORK/B_$MOD.sv"
python3 "$HERE/gen_lockstep.py" "$HEAD/srp/$MOD.sv" "$MOD" "$NP" "$N" "$WORK"
cp "$HERE/drive.hpp" "$HERE/ls_main.cpp" "$WORK/"
"$VERILATOR" --cc --exe --build -j 4 --top-module ls_wrap -Wno-fatal -Wno-lint -Wno-style \
  --x-assign unique --x-initial unique -CFLAGS "-std=c++17 -O2 -I$WORK ${LS_CFLAGS:-}" --Mdir "$WORK/obj" \
  "$HEAD/common/pp_pkg.sv" "$HEAD/srp/srp_pkg.sv" "$WORK/B_$MOD.sv" "$HEAD/srp/$MOD.sv" \
  "$WORK/ls_wrap.sv" "$WORK/ls_main.cpp" "$WORK/drive_gen.cpp" -o Vls > "$WORK/build.log" 2>&1
rc=0
for seed in "$@"; do
  "$WORK/obj/Vls" "$seed" "$CYC" +verilator+rand+reset+2 +verilator+seed+"$seed" > "$WORK/run-$seed.log" 2>&1 || rc=1
  echo "$MOD N=$N seed=$seed: $(head -n 20 "$WORK/run-$seed.log" | grep '^seed')"
done
exit $rc
