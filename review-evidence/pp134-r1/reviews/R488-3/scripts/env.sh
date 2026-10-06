# Shared environment for the R488-3 probes. Paths are relative to the packet root ($P).
P=${P:-$REVIEWS/pp134-r488-3-packet}
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
export TMPDIR=$P/scratch/tmp
mkdir -p "$TMPDIR"
