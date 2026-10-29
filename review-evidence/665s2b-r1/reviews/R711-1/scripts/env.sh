# Environment for the reviewer's runs (sourced): product LiteX venv, pinned RV32 SDK, pinned Verilator 5.050, offline generator.
export PATH=${TOOLS:?set TOOLS to the pinned tools directory}/pinned-verilator-5.050:$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
