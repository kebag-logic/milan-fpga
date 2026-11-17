# Environment for the lane's harness and firmware runs (sourced): the product LiteX tree's venv, the pinned RV32 SDK,
# the offline CPU generator, the board launcher's hash seed, the pinned Verilator, sv2v and make.
export PATH=<home>/litex-milan/venv/bin:<home>/br-milan-rv32/host/bin:<installed-tool>
export VERILATOR=<installed-tool>
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
