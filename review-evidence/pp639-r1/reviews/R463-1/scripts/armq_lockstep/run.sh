#!/usr/bin/env bash
# Arm-port lockstep. Usage: run.sh REPO OUTDIR [MUTANT]
#   builds main 5c71928a's block (reference) beside the head's (candidate), one model per
#   slot width (5, 6 = 1x1, 7 = 8x8, 8), runs 8 seeds x 1,000,000 cycles per width.
set -euo pipefail
REPO=$1; OUT=$2; MUT=${3:-}
V=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
HERE=$(cd "$(dirname "$0")" && pwd)
BASE=5c71928ad2bf1a854a5538d69b77214dfdf1697f
HEAD=9e8699105c126db7764820916a827ef0538bc4b2
CYC=${CYCLES:-1000000}
mkdir -p "$OUT"; OUT=$(cd "$OUT" && pwd)
git -C "$REPO" show $BASE:hdl/top/protocol_processor_top.sv > "$OUT/top_main.sv"
git -C "$REPO" show $HEAD:hdl/top/protocol_processor_top.sv > "$OUT/top_head.sv"
python3 "$HERE/extract.py" "$OUT/top_main.sv" armq_ref "$OUT/armq_ref.sv" 2> "$OUT/extract.log"
if [ -n "$MUT" ]; then
  python3 "$HERE/extract.py" "$OUT/top_head.sv" armq_dut "$OUT/armq_dut.sv" --mutate "$MUT" 2>> "$OUT/extract.log"
else
  python3 "$HERE/extract.py" "$OUT/top_head.sv" armq_dut "$OUT/armq_dut.sv" 2>> "$OUT/extract.log"
fi
: > "$OUT/results.txt"
for AW in 5 6 7 8; do
  B="$OUT/obj_aw$AW"
  "$V" --cc --exe --build -j 2 -O3 --x-assign unique --x-initial unique -Wno-fatal -Wno-lint -Wno-style \
       --top-module armq_ls -GAW=$AW -Mdir "$B" "$OUT/armq_ref.sv" "$OUT/armq_dut.sv" \
       "$HERE/armq_ls.sv" "$HERE/bench.cpp" -o Varmq_ls > "$OUT/build_aw$AW.log" 2>&1
  for S in 1 2 3 4 5 6 7 8; do
    set +e
    "$B/Varmq_ls" $((AW * 100 + S)) "$CYC" "$AW" >> "$OUT/results.txt"
    echo "rc=$? aw=$AW seed=$((AW * 100 + S))" >> "$OUT/results.txt"
    set -e
  done
done
