#!/bin/sh
# Run a harness command with the offline LiteX/toolchain environment.
# Usage: env_run.sh <repo> <args to run.py...>; WS defaults to $HOME.
WS=${WS:-$HOME}
REPO=$1; shift
cd "$REPO" || exit 2
exec env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true \
  LITEX_ENV_CC_TRIPLE=riscv32-linux PATH="$WS/litex-milan/venv/bin:/usr/bin:/bin:$WS/br-milan-rv32/host/bin" \
  "$WS/litex-milan/venv/bin/python" -B tb/verilator/fw_service_budget/run.py "$@"
