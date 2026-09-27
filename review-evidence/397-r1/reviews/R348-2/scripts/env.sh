# Environment for product-CPU builds (same as round 1). Set LITEX_VENV to the
# product LiteX virtualenv (pinned revisions, product patches applied, cached
# CPU netlist) and RV32_SDK to the RV32 SDK root before sourcing.
: "${LITEX_VENV:?set LITEX_VENV}" "${RV32_SDK:?set RV32_SDK}"
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export LITEX_ENV_CC_TRIPLE=riscv32-linux
export PATH=$LITEX_VENV/bin:/usr/bin:/bin:$RV32_SDK/host/bin:$RV32_SDK/bin
