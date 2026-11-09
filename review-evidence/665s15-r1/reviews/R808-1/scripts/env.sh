# Sourced: the product LiteX venv, the pinned RV32 SDK, the pinned Verilator 5.050, sv2v, make 4.3,
# the hash seed and the offline CPU generator. DATA is the tools root.
DATA=${DATA:-$VALIDATION_STORAGE}
export PATH=$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin:$DATA/tools/pinned-verilator-5.050:$DATA/tools/sv2v-v0.0.12:$DATA/scratch/a662/make43/bin:$PATH
export VERILATOR=$DATA/tools/pinned-verilator-5.050/verilator
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
