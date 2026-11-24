# The parent's tool environment: pinned RV32 SDK (read only), pinned Verilator 5.050, offline netlist.
S=/data-2/milan/tmp/lwsrppin-a834; SDK=/data-2/milan/tmp/s12b-a783<home-path>
V=$VALIDATION_TOOLS/pinned-verilator-5.050
export HOME=$S/home TMPDIR=$S/tmpdir VERILATOR=$V/verilator PYTHONHASHSEED=0
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=riscv32-linux
export PATH=$WORKSPACE_HOME/litex-milan/venv/bin:$V:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin:$SDK/host/bin
export TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c GIT_ALLOW_PROTOCOL=file:https
