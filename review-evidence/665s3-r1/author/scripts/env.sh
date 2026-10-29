# The lane's environment for the LiteX and RV32 steps (sourced).
export PATH=$WORKSPACE_HOME/litex-milan/venv/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
