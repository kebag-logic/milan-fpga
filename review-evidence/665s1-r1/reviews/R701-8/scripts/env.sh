# Sourced by the probe scripts: the LiteX venv and pinned RV32 SDK, offline generator, fixed hash seed.
# CHECKOUT is the review clone at the exact head; PACKET is this packet.
export PATH=$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
: "${CHECKOUT:=$REVIEWS/r701-8-665s1}"
: "${PACKET:=$REVIEWS/665s1-r701-8-packet}"
export TMPDIR=$PACKET/scratch/tmp; mkdir -p "$TMPDIR"
