#!/usr/bin/env bash
# One CPU service-budget harness run in a given tree, with the review's tool environment.
# Usage: harness.sh <receipt-dir> <tree> <build-dir> <run.py args...>
# Tools: the product LiteX venv, the verified pinned RV32 SDK (ci_rv32_sdk.py --verify-only) and the pinned
# Verilator 5.050 wrapper, first on PATH.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
out=$1; tree=$2; build=$3; shift 3
: "${REVIEW_VBIN:?the directory holding the pinned verilator}"
: "${REVIEW_SDK_BIN:?the verified SDK bin}"
: "${REVIEW_LITEX_BIN:?the LiteX venv bin}"
export PATH="$REVIEW_VBIN:$REVIEW_LITEX_BIN:$REVIEW_SDK_BIN:/usr/local/bin:/usr/bin:/bin"
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
"$here/launch.sh" "$out" "$tree" python3 -B tb/verilator/ctrl_service_budget/run.py --build-dir "$build" "$@"
