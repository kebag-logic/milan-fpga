# env.sh: this lane's tool environment, the gating recipe's (S12b gating lane tools/env.sh) with HOME and TMPDIR in this
# lane's scratch; the gating lane's pinned RV32 SDK, read only (the bench images' firmware was compiled with it)
S=<scratch>; SDK=<host-tmp>/s12b-a783<home-path>
V=<host-tools>/tools/pinned-verilator-5.050
export HOME=$S/home TMPDIR=$S/tmp VERILATOR=$V/verilator PYTHONHASHSEED=0
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=riscv32-linux
export PATH=<home>/litex-milan/venv/bin:$V:<host-tools>/tools/sv2v-v0.0.12:<host-tools>/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin:$SDK/host/bin
export TSN_GEN_ROOT=<home>/milan-fpga-management/tools/tsn-gen-deca300c GIT_ALLOW_PROTOCOL=file:https
