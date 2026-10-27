# Environment for the lane's harness runs (sourced): the product LiteX tree's venv, the pinned RV32 SDK,
# the offline CPU generator, and the board launcher's hash seed.
export PATH=$WORKSPACE_HOME/litex-milan/venv/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
