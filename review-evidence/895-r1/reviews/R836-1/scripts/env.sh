# Reviewer environment (sourced): the product LiteX tree's venv, the pinned RV32 SDK, pinned Verilator 5.050 and sv2v,
# the offline CPU generator, the hash seed. Set TOOLS to the directory holding pinned-verilator-5.050 and sv2v-v0.0.12.
: "${TOOLS:?set TOOLS to the pinned tool directory}"
export PATH=$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin:$TOOLS/pinned-verilator-5.050:$TOOLS/sv2v-v0.0.12:$PATH
export VERILATOR=$TOOLS/pinned-verilator-5.050/verilator
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
