#!/usr/bin/env bash
# The firmware service-budget simulations gen_oracle.py converts
# (tb/verilator/fw_service_budget/README.md "Run and reproduce"): both shapes'
# builds, the `all` plan on each and `uart-paced` on the 1x1, populated, in a
# network namespace with the product environment.
# The dev-baseline subset (the 1x1 `all` plan only). Usage: svc_driver_dev.sh <repo> <scratch>
set -u
repo=$1; scratch=$2
export PRODUCT_PYTHON="$HOME/litex-milan/venv/bin/python"
export PYTHON="$PRODUCT_PYTHON"
export LITEX_ENV_CC_TRIPLE=riscv32-linux
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
export PATH="/usr/local/bin:/usr/bin:/bin:$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin"
export TMPDIR="$scratch/tmp"
mkdir -p "$TMPDIR"
cd "$repo" || exit 2
step() {
  local name=$1; shift
  echo "START $name $(date -Is)"
  unshare -Urn "$PRODUCT_PYTHON" -B tb/verilator/fw_service_budget/run.py "$@" > "$scratch/run-$name.log" 2>&1
  echo "END $name rc=$? $(date -Is)"
}
step 1x1-build --shape endstation_ax7101_1x1_tdm8 --build-dir "$scratch/fw-1x1" --build-only
step 1x1-all --shape endstation_ax7101_1x1_tdm8 --build-dir "$scratch/fw-1x1" --reuse-build --populated --record-budget-findings



