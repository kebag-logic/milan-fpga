#!/bin/sh
# Reproduce one nvm_capture_cpu arm at the exact head, following
# tb/verilator/nvm_capture_cpu/README.md: offline, network namespace disabled,
# PYTHONHASHSEED=0, external build directory, 16 captures.
# Usage: reproduce_capture.sh <repo> <packet> <shape-suffix> <cpu-hz> <on|off>
# Environment: SDK_BIN (pinned RV32 SDK bin), LITEX_VENV_BIN (LiteX venv bin).
set -eu
repo=$1; packet=$2; shape=$3; hz=$4; arm=$5
label="$shape-$((hz / 1000000))-$arm"
build="$packet/scratch/capture-$label"
log="$packet/receipts/capture-$label.log"
rm -rf "$build"
cd "$repo"
export PATH="$SDK_BIN:$LITEX_VENV_BIN:$PATH"
export LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0 \
       COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
{
  echo "HEAD $(git rev-parse HEAD)"
  echo "VERILATOR $(verilator --version)"
  echo "START $(date -Is)"
  set +e
  unshare -Urn python3 tb/verilator/nvm_capture_cpu/run.py \
    --shape "endstation_ax7101_$shape" --cpu-hz "$hz" --captures 16 \
    --traffic "$arm" --build-dir "$build"
  rc=$?
  set -e
  echo "END $(date -Is) rc=$rc"
} > "$log" 2>&1
[ -f "$build/capture.log" ] && cp "$build/capture.log" "$packet/receipts/rows-$label.log"
[ -f "$build/measurement.json" ] && cp "$build/measurement.json" "$packet/receipts/measurement-$label.json"
echo "$rc" > "$packet/receipts/capture-$label.rc"
