# Reviewer environment: the product LiteX venv and the pinned RV32 SDK, offline.
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
