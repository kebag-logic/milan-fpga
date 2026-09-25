#!/usr/bin/env bash
# Focused composed-suite runs for #443 on the merge-train candidate.
# Usage: run_focused_suites.sh <clone> <receipts-dir> <pinned-verilator-dir>
set -u
CLONE=${1:?clone}
OUT=${2:?receipts dir}
VDIR=${3:?dir holding the pinned verilator}
export PATH="$VDIR:$PATH"
mkdir -p "$OUT"
cd "$CLONE" || exit 2
run() {
  local name=$1; shift
  local t0=$SECONDS
  "$@" >"$OUT/$name.log" 2>&1
  local rc=$?
  printf '%-28s rc=%d  %4ds  %s\n' "$name" "$rc" "$((SECONDS - t0))" "$*" | tee -a "$OUT/SUMMARY.txt"
}
: >"$OUT/SUMMARY.txt"
echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree}) verilator $(command -v verilator): $(verilator --version)" | tee -a "$OUT/SUMMARY.txt"
run csr                  make -C tb/verilator/csr VERILATOR_JOBS=8
run crf_rx               make -C tb/verilator/crf_rx VERILATOR_JOBS=8
run milan_dp_aclk        make -C tb/verilator/milan_dp aclk VERILATOR_JOBS=8
run render_csr_controls  make -C tb/verilator/milan_dp render-csr-controls VERILATOR_JOBS=8
run milan_dp_render      make -C tb/verilator/milan_dp_render VERILATOR_JOBS=8
