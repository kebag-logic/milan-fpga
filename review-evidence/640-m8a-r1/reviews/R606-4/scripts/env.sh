# Source me. Disposable environment for this review: everything under $PACKET/scratch.
# PACKET: this packet; CLONE: the detached clone at the reviewed head.
: "${PACKET:?}" "${CLONE:?}"
S=$PACKET/scratch
export HOME=$S/home                       # holds br-milan-rv32/host (fresh, verified) and copied sbt caches
export MILAN_RV32_CC=$HOME/br-milan-rv32/host/bin/riscv32-linux-gcc
export PYTHONHASHSEED=0 TMPDIR=$S/tmp
mkdir -p "$TMPDIR"
# $S/bin: pinned sv2v v0.0.12 and the pinned Verilator 5.050 wrapper
export PATH=$S/bin:$PATH
