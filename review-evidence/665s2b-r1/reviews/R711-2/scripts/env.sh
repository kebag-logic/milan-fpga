# Environment for the reviewer's harness probes (sourced). The caller sets WORKSPACE_HOME (the product LiteX tree's
# and the RV32 SDK's parent) and VALIDATION_TOOLS (the pinned simulator and sv2v).
: "${WORKSPACE_HOME:?}" "${VALIDATION_TOOLS:?}"
export PATH=$WORKSPACE_HOME/litex-milan/venv/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$PATH
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
export PYTHONDONTWRITEBYTECODE=1
