#!/bin/sh
# Environment for the review's focused runs. Set, before sourcing:
#   VERILATOR_DIR  the directory holding the pinned Verilator 5.050 `verilator`
#   RV32_BIN       the pinned RV32 SDK's bin directory (riscv32-linux-gcc)
#   LITEX_PY       the product LiteX tree's Python interpreter (it carries PyYAML)
: "${VERILATOR_DIR:?set VERILATOR_DIR}" "${RV32_BIN:?set RV32_BIN}" "${LITEX_PY:?set LITEX_PY}"
PATH="$VERILATOR_DIR:$RV32_BIN:$PATH"
LITEX_ENV_CC_TRIPLE=riscv32-linux
PYTHONHASHSEED=0
COURSIER_MODE=offline
SBT_OPTS=-Dsbt.offline=true
export PATH LITEX_ENV_CC_TRIPLE PYTHONHASHSEED COURSIER_MODE SBT_OPTS LITEX_PY
