# Environment for product-CPU builds. Set LITEX_VENV to the LiteX virtualenv
# (pinned product LiteX revisions with sw/litex/patches applied and the cached
# CPU netlist) and RV32_SDK to the RV32 SDK root before sourcing.
: "${LITEX_VENV:?set LITEX_VENV}" "${RV32_SDK:?set RV32_SDK}"
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export LITEX_ENV_CC_TRIPLE=riscv32-linux
export PATH=$LITEX_VENV/bin:/usr/bin:/bin:$RV32_SDK/host/bin
