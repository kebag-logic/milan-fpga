# env.sh: the S12b gating lane's tool environment (its tools/env.sh), HOME and TMPDIR moved to train1117-a794's scratch; the pinned RV32 SDK in that lane's scratch, read only
S=<scratch>/gate13; SDK=<gating-sdk>
V=<tools>/pinned-verilator-5.050
export HOME=<scratch>/home TMPDIR=$S/tmp VERILATOR=$V/verilator PYTHONHASHSEED=0
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=riscv32-linux
export PATH=<home>/litex-milan/venv/bin:$V:<tools>/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin:$SDK/host/bin
export TSN_GEN_ROOT=<management>/tools/tsn-gen-deca300c GIT_ALLOW_PROTOCOL=file:https
