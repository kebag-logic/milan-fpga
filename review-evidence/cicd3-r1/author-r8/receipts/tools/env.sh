export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export PATH=$WORKSPACE_HOME/litex-milan/venv/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TMPDIR=/data-2/milan/tmp/cicd-a839/tmp
mkdir -p "$TMPDIR"
