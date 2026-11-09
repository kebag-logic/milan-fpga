# Environment for the lane's harness and firmware runs (sourced): the product LiteX tree's venv, the pinned RV32 SDK,
# the offline CPU generator, the hash seed, the pinned Verilator, sv2v and make.
export PATH=<litex-venv>/bin:<rv32-sdk>/host/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<tools-scratch>/a662/make43/bin:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
