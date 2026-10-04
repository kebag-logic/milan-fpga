#!/usr/bin/env bash
# Listener lockstep. Usage: run.sh REPO OUTDIR [MUTANT]
#   main 5c71928a's KL_pp_acmp_listener (renamed _ref) beside the head's, one model per
#   N_SINKS_P (1, 2 = 1x1, 3, 8, 9 = 8x8), 8 seeds x CYCLES (default 1,000,000) each.
set -euo pipefail
REPO=$1; OUT=$2; MUT=${3:-}
V=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
HERE=$(cd "$(dirname "$0")" && pwd)
BASE=5c71928ad2bf1a854a5538d69b77214dfdf1697f
HEAD=9e8699105c126db7764820916a827ef0538bc4b2
CYC=${CYCLES:-1000000}
SINKS=${SINKS:-"1 2 3 8 9"}
mkdir -p "$OUT"; OUT=$(cd "$OUT" && pwd)
L=hdl/acmp/KL_pp_acmp_listener.sv
for f in hdl/common/pp_pkg.sv hdl/acmp/pp_acmp_pkg.sv; do
  # the two packages must be byte-identical at both revisions
  cmp <(git -C "$REPO" show $BASE:$f) <(git -C "$REPO" show $HEAD:$f)
done
git -C "$REPO" show $HEAD:hdl/common/pp_pkg.sv > "$OUT/pp_pkg.sv"
git -C "$REPO" show $HEAD:hdl/acmp/pp_acmp_pkg.sv > "$OUT/pp_acmp_pkg.sv"
git -C "$REPO" show $BASE:$L | sed 's/^module KL_pp_acmp_listener$/module KL_pp_acmp_listener_ref/; s/^endmodule : KL_pp_acmp_listener$/endmodule : KL_pp_acmp_listener_ref/' > "$OUT/lsn_ref.sv"
grep -q '^module KL_pp_acmp_listener_ref$' "$OUT/lsn_ref.sv"
git -C "$REPO" show $HEAD:$L > "$OUT/lsn_dut.sv"
cmp <(git -C "$REPO" show $BASE:hdl/acmp/rom/gen_ltn_rom.py) <(git -C "$REPO" show $HEAD:hdl/acmp/rom/gen_ltn_rom.py)
git -C "$REPO" show $HEAD:hdl/acmp/rom/gen_ltn_rom.py > "$OUT/gen_ltn_rom.py"
python3 "$OUT/gen_ltn_rom.py" -o "$OUT/ltn_rom.hex" > /dev/null
if [ -n "$MUT" ]; then python3 "$HERE/mutate.py" "$OUT/lsn_dut.sv" "$MUT"; fi
python3 "$HERE/gen_wrap.py" "$OUT/lsn_dut.sv" "$OUT/lsn_ls.sv" 2> "$OUT/gen.log"
sha256sum "$OUT"/lsn_ref.sv "$OUT"/lsn_dut.sv "$OUT"/ltn_rom.hex > "$OUT/inputs.sha256"
: > "$OUT/results.txt"
for N in $SINKS; do
  B="$OUT/obj_n$N"
  "$V" --cc --exe --build -j 2 -O3 --x-assign unique --x-initial unique -Wno-fatal -Wno-lint -Wno-style \
       --top-module lsn_ls -GN_SINKS_P=$N -GSTO=64 -Mdir "$B" "$OUT/pp_pkg.sv" "$OUT/pp_acmp_pkg.sv" \
       "$OUT/lsn_ref.sv" "$OUT/lsn_dut.sv" "$OUT/lsn_ls.sv" "$HERE/bench.cpp" -o Vlsn_ls \
       > "$OUT/build_n$N.log" 2>&1
  for S in 1 2 3 4 5 6 7 8; do
    set +e
    (cd "$OUT" && "$B/Vlsn_ls" $((N * 100 + S)) "$CYC" "$N") >> "$OUT/results.txt"
    echo "rc=$? n=$N seed=$((N * 100 + S))" >> "$OUT/results.txt"
    set -e
  done
done
