# Source to reproduce the capture measurement environment.
# Required: LITEX_TREE (product LiteX tree at the receipt's revisions), SDK_BIN (pinned RV32 SDK bin),
# CCBIN (directory mapping riscv32-linux-* to the SDK's tools).
: "${LITEX_TREE:?}" "${SDK_BIN:?}" "${CCBIN:?}"
PYTHONPATH=""
for d in "$LITEX_TREE"/litex "$LITEX_TREE"/migen "$LITEX_TREE"/lite* "$LITEX_TREE"/pythondata-*; do
  [ -d "$d" ] && PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$d"
done
export PYTHONPATH PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
export LITEX_ENV_CC_TRIPLE=riscv32-linux COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export PATH="$CCBIN:/usr/bin:/bin:$SDK_BIN"  # SDK last: its bin ships its own python3
