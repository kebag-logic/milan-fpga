#!/usr/bin/env bash
# Run the composition gates at the merge-train candidate concurrently, one log
# and one rc file per gate. Usage:
#   run_candidate_gates.sh <candidate-worktree> <receipts-dir> <build-scratch>
# Environment it reads (all optional, each named in the receipt):
#   LITEX_PY   interpreter that imports migen + litex
#   RV32_CC    pinned RV32 compiler (verified with scripts/ci_rv32_sdk.py)
#   VL_DIR     directory holding the pinned verilator wrapper
#   PY         interpreter for the repository gates (carries the pinned Markdown renderer)
set -uo pipefail
WT=$(cd "$1" && pwd); OUT=$(mkdir -p "$2" && cd "$2" && pwd); BS=$(mkdir -p "$3" && cd "$3" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
LITEX_PY=${LITEX_PY:-python3}; PY=${PY:-python3}; RV32_CC=${RV32_CC:-riscv32-linux-gcc}; VL_DIR=${VL_DIR:-}
BASE=e282ecd2691bdf2018d31376d3930c984a2c0499
cd "$WT" || exit 2
{
  echo "worktree=$WT head=$(git rev-parse HEAD) tree=$(git rev-parse 'HEAD^{tree}')"
  echo "py=$PY litex_py=$LITEX_PY rv32_cc=$RV32_CC vl_dir=$VL_DIR"
  [ -n "$VL_DIR" ] && "$VL_DIR/verilator" --version
} > "$OUT/env.txt" 2>&1
[ -n "$VL_DIR" ] && export PATH="$VL_DIR:$PATH"
export MILAN_RV32_CC="$RV32_CC" MILAN_LITEX_PYTHON="$LITEX_PY" COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export CC_MAP="$OUT/builder_cc_map.jsonl"

run() {  # name, command...
  local name=$1; shift
  ( start=$(date +%s); "$@" > "$OUT/$name.log" 2>&1; rc=$?
    echo "$rc $(( $(date +%s) - start ))s" > "$OUT/$name.rc" ) &
}

run py_idiom          "$PY" scripts/check_py_idiom.py
run docs_check        "$PY" scripts/docs_check.py
run doc_style         "$PY" scripts/check_doc_style.py
run doc_paths         "$PY" scripts/check_doc_paths.py
run toc_check         "$PY" scripts/gen_toc.py --check
run toc_anchors       "$PY" scripts/gen_toc.py --verify-anchors
run em_dash           "$PY" scripts/check_em_dash.py --base "$BASE"
run solution_docs     "$PY" scripts/check_solution_docs.py
run archive           "$PY" scripts/check_archive.py
run hygiene           "$PY" scripts/check_hygiene.py --check
run diff_check        git diff --check "$BASE" HEAD
run ctrl_memory       "$LITEX_PY" -B sw/litex/test_ctrl_memory.py
run builder_subset    "$PY" -B "$HERE/builder_pinned_cc.py" "$RV32_CC" \
      --gates test_control_placement_key,test_placement_recipe,test_image_identity_gate,test_nvm_firmware_shapes,test_name_count_fits_the_nvm_name_block,test_split_record_space_bounds_the_split_output \
      --require-rv32 --receipt "$OUT/builder_subset.receipt.json"
run split_boot_1x1    "$LITEX_PY" -B tb/verilator/ctrl_split_boot/run.py --build-dir "$BS/split-boot-1x1"
wait
for f in "$OUT"/*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done | sort > "$OUT/summary.txt"
cat "$OUT/summary.txt"
