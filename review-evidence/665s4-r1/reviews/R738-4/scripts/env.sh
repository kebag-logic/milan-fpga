# Probe environment: the product LiteX venv, the workstation RV32 SDK, the scoped Verilator 5.050.
export SDK=$HOME/br-milan-rv32/host
export LITEX_PY=$HOME/litex-milan/venv/bin
export PATH="$VALIDATION_TOOLS/pinned-verilator-5.050:$LITEX_PY:$SDK/bin:/usr/local/bin:/usr/bin:/bin"
export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
