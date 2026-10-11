#!/usr/bin/env bash
# Runs arms of the saved-state capture matrix of
# tb/verilator/nvm_capture_cpu/README.md one after another, in a network
# namespace, with the receipt's environment.
# Usage: capture_driver.sh <repo> <scratch> <arm>...   arm = <shape-tag>-<mhz>-<traffic>
set -u
repo=$1; scratch=$2; shift 2
export PRODUCT_PYTHON="$HOME/litex-milan/venv/bin/python"
export PYTHON="$PRODUCT_PYTHON"
export LITEX_ENV_CC_TRIPLE=riscv32-linux
export PYTHONHASHSEED=0
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
export PATH="$HOME/litex-milan/venv/bin:/usr/local/bin:/usr/bin:/bin:$HOME/br-milan-rv32/host/bin"
export TMPDIR="$scratch/tmp"
mkdir -p "$TMPDIR"
cd "$repo" || exit 2
for arm in "$@"; do
  IFS=- read -r tag mhz traffic <<<"$arm"
  case $tag in
    8x8) shape=endstation_ax7101_8x8 ;;
    1x1) shape=endstation_ax7101_1x1_tdm8 ;;
    *) echo "bad arm $arm"; exit 2 ;;
  esac
  build="$scratch/$arm/capture-$arm"
  rm -rf "$build"
  mkdir -p "$scratch/$arm"
  echo "START $arm $(date -Is)"
  unshare -Urn "$PRODUCT_PYTHON" -B tb/verilator/nvm_capture_cpu/run.py \
    --shape "$shape" --cpu-hz "${mhz}000000" --captures 16 \
    --traffic "$traffic" --build-dir "$build" > "$scratch/run-$arm.log" 2>&1
  echo "END $arm rc=$? $(date -Is)"
done
