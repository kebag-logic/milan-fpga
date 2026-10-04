#!/usr/bin/env bash
# build one lockstep binary: run.sh REF_TOP HEAD_TOP AW OUTDIR [MUTANT]
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
ref=$1; head=$2; aw=$3; out=$4; mut=${5:-}
mkdir -p "$out"
python3 "$here/gen.py" "$ref" armq_ref "$out/armq_ref.sv"
if [ -n "$mut" ]; then
  python3 "$here/gen.py" "$head" armq_dut "$out/armq_dut.sv" --mutant "$mut"
else
  python3 "$here/gen.py" "$head" armq_dut "$out/armq_dut.sv"
fi
verilator --cc --exe --build -j 4 -O3 --x-initial unique --x-assign unique \
  -Wno-fatal -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -GAW="$aw" -CFLAGS "-O2 -std=c++17 -DAW_BITS=$aw" --top-module lock_top \
  --Mdir "$out/obj" "$out/armq_ref.sv" "$out/armq_dut.sv" "$here/lock_top.sv" "$here/lock_main.cpp" \
  -o Vlock_top > "$out/build.log" 2>&1
