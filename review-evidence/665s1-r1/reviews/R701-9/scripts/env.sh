# Sourced: the product LiteX venv, the pinned RV32 SDK, pinned Verilator 5.050, offline generator.
# Override LITEX_VENV, RV32_SDK, VERILATOR_BIN as needed.
: "${LITEX_VENV:=$HOME/litex-milan/venv}" "${RV32_SDK:=$HOME/br-milan-rv32/host}"
: "${VERILATOR_BIN:=$VALIDATION_TOOLS/pinned-verilator-5.050}"
export PATH=$VERILATOR_BIN:$LITEX_VENV/bin:$RV32_SDK/bin:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu PYTHONHASHSEED=0
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
