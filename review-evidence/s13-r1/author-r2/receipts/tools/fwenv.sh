# fwenv.sh: the firmware and harness environment (the train's bin/env.sh): the product LiteX venv, the pinned RV32 SDK,
# the offline CPU generator, the hash seed, the pinned Verilator, sv2v and make; HOME and TMPDIR in this lane's scratch
export PATH=<home>/litex-milan/venv/bin:<home>/br-milan-rv32/host/bin:<host-tools>/tools/pinned-verilator-5.050:<host-tools>/tools/sv2v-v0.0.12:<host-tools>/scratch/a662/make43/bin:$PATH
export VERILATOR=<host-tools>/tools/pinned-verilator-5.050/verilator
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export HOME=<scratch>/home TMPDIR=<scratch>/tmp
