# Environment for the lane's firmware, image and harness runs (sourced): the product LiteX tree's venv, the pinned
# RV32 SDK, the offline CPU generator, the hash seed, the pinned Verilator, sv2v and make (as #810's lanes use).
export PATH=<home>/litex-milan/venv/bin:<home>/br-milan-rv32/host/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<scratch2>/a662/make43/bin:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
export TMPDIR=<scratch>/tmp
