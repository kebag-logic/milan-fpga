#!/bin/bash
set -eu
packet=$(cd "$(dirname "$0")" && pwd)
export REVIEW_PACKET="$packet"
export REVIEW_ROOT="${REVIEW_ROOT:-$PWD}"
export TMPDIR="$packet/scratch"
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
export PYTHONPATH="$packet/scratch/python${PYTHONPATH:+:$PYTHONPATH}"
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
: "${PRODUCT_PYTHON:?Set PRODUCT_PYTHON to the product environment Python}"
: "${MILAN_RV32_CC:?Set MILAN_RV32_CC to the RV32 compiler}"
: "${PINNED_SIM_DIR:?Set PINNED_SIM_DIR to the verified simulator directory}"
export LITEX_ENV_CC_TRIPLE="${LITEX_ENV_CC_TRIPLE:-riscv32-linux}"
export PATH="$packet/scratch/bin:$PINNED_SIM_DIR:$(dirname "$MILAN_RV32_CC"):$PATH"
exec "$PRODUCT_PYTHON" -B "$@"
