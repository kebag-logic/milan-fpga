# Probe environment (sourced): product LiteX venv, pinned RV32 SDK, pinned Verilator 5.050 first on PATH.
S=$REVIEWS/665s2b-r712-4-packet/scratch
export PATH=$S/vbin:$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
