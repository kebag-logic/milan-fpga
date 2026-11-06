# Probe environment: the product LiteX tree's python, the gate environment's RV32 SDK, the scoped Verilator 5.050.
export PATH=$VERILATOR_DIR:$LITEX_ENV/bin:$RV32_SDK/bin:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
