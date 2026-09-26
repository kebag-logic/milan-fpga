#!/usr/bin/env bash
# Run the assigned default targets in a disposable copy of the exact head.
# Usage: run_suites.sh <tree> <out-dir>
set -uo pipefail
tree=$1 out=$2
: "${PYVENV:=$VALIDATION_TOOLS/md-venv-40cdefe08ebd}"
: "${SDK_BIN:=$HOME/br-milan-rv32/host/bin}"
export PATH="$PYVENV/bin:$PATH:$SDK_BIN"
mkdir -p "$out"
cd "$tree" || exit 2
summary="$out/suites-summary.txt"
: > "$summary"
step() {
  local name=$1; shift
  local t0=$SECONDS
  bash -c "$*" > "$out/$name.log" 2>&1
  local rc=$?
  printf 'rc=%d %4ds | %s | %s\n' "$rc" $((SECONDS - t0)) "$name" "$*" | tee -a "$summary"
}
echo "head $(git rev-parse HEAD) verilator $(verilator --version)" | tee -a "$summary"
step declarations 'python3 sw/builder/test_declarations.py'
step nvm_hosttest 'python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test'
step csr 'make -C tb/verilator/csr'
step pp_shadow 'make -C tb/verilator/pp_shadow'
step nvm_cosim 'make -C tb/verilator/nvm_cosim'
step capture_gate 'python3 scripts/check_nvm_capture.py'
for m in bytes records clock ignore-off-timing; do
  step "capture_mut_$m" "python3 scripts/check_nvm_capture.py --mutation $m; test \$? -ne 0"
done
