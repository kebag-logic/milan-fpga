# Environment for the harness and firmware runs (sourced): product LiteX venv, pinned RV32 SDK,
# pinned Verilator 5.050, sv2v, make 4.3, hash seed, offline JVM tools.
D=${DATA:?set DATA to the tools root (holding tools/ and scratch/a662/make43)}
export PATH=$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin:$D/tools/pinned-verilator-5.050:$D/tools/sv2v-v0.0.12:$D/scratch/a662/make43/bin:$PATH
export VERILATOR=$D/tools/pinned-verilator-5.050/verilator
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
