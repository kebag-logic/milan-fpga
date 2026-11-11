#!/usr/bin/env bash
# Run the split boot simulation at one checkout for the given shapes,
# concurrently, with a fixed Python hash seed (LiteX's VexiiRiscv ISA string is
# built from a set, so two exports in two processes can spell it differently).
# Usage: run_split_boot.sh <checkout> <receipts-dir> <build-scratch> <shape>...
# Environment: LITEX_PY, RV32_CC, VL_DIR as in run_candidate_gates.sh.
set -uo pipefail
WT=$(cd "$1" && pwd); OUT=$(mkdir -p "$2" && cd "$2" && pwd); BS=$(mkdir -p "$3" && cd "$3" && pwd); shift 3
LITEX_PY=${LITEX_PY:-python3}; RV32_CC=${RV32_CC:-riscv32-linux-gcc}; VL_DIR=${VL_DIR:-}
[ -n "$VL_DIR" ] && export PATH="$VL_DIR:$PATH"
export MILAN_RV32_CC="$RV32_CC" COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true PYTHONHASHSEED=0
cd "$WT" || exit 2
echo "checkout=$WT head=$(git rev-parse HEAD) litex_py=$LITEX_PY rv32_cc=$RV32_CC vl_dir=$VL_DIR PYTHONHASHSEED=0" > "$OUT/split_boot_env.txt"
for shape in "$@"; do
  ( start=$(date +%s)
    "$LITEX_PY" -B tb/verilator/ctrl_split_boot/run.py --build-dir "$BS/split-boot-$shape" --shape "$shape" \
      > "$OUT/split_boot_$shape.log" 2>&1
    echo "$? $(( $(date +%s) - start ))s" > "$OUT/split_boot_$shape.rc" ) &
done
wait
for shape in "$@"; do echo "split_boot_$shape $(cat "$OUT/split_boot_$shape.rc")"; done
