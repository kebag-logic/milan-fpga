# Shared environment for the R532-8 runs (source it). Override PACKET (this
# packet), CLONE (a clean checkout of the exact head with lwSRP, protocol-processor
# and gptp-processor initialized) and TOOLS as needed.
P=${PACKET:-$REVIEWS/665f4-r532-8-packet}; R=${CLONE:-$REVIEWS/r532-8-665f4}; S=$P/scratch
export MILAN_RV32_CC=$S/sdk/bin/riscv32-linux-gcc PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S/tmp
