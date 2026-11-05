#!/usr/bin/env bash
# After the 13:10 host reset of 2026-11-05: the three simulations it killed, on the same
# 551ba236 clones and environment as svc_driver.sh and capture_driver.sh.
#   - the 8x8 service-budget `all` plan, reusing the completed 8x8 build;
#   - the capture arms 8x8-100-on and 8x8-100-off, each from a fresh build directory.
# Usage: resume_after_reset.sh <svc-repo> <svc-scratch> <cap-repo> <cap-scratch>
set -u
svc_repo=$1; svc=$2; cap_repo=$3; cap=$4
here=$(dirname "$(readlink -f "$0")")
(
  export PRODUCT_PYTHON="$HOME/litex-milan/venv/bin/python"
  export PYTHON="$PRODUCT_PYTHON"
  export LITEX_ENV_CC_TRIPLE=riscv32-linux
  export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
  export COURSIER_MODE=offline
  export SBT_OPTS=-Dsbt.offline=true
  export PATH="/usr/local/bin:/usr/bin:/bin:$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin"
  export TMPDIR="$svc/tmp"
  mkdir -p "$TMPDIR"
  cd "$svc_repo" || exit 2
  echo "START 8x8-all $(date -Is)"
  unshare -Urn "$PRODUCT_PYTHON" -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 \
    --build-dir "$svc/fw-8x8" --reuse-build --populated --record-budget-findings > "$svc/run-8x8-all.log" 2>&1
  echo "END 8x8-all rc=$? $(date -Is)"
) > "$svc/chain-8x8-resume.log" 2>&1 &
"$here/capture_driver.sh" "$cap_repo" "$cap" 8x8-100-on 8x8-100-off > "$cap/driver-resume.log" 2>&1 &
wait
echo "ALL DONE $(date -Is)"
