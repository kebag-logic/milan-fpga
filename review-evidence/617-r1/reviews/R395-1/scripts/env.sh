# source me: pinned simulator first on PATH, 8-job cap, temp dirs in scratch
P=$REVIEWS/617-r395-1-packet
export REAL_VERILATOR=$VALIDATION_TOOLS/verilator-v5.050-src/bin/verilator
export PATH="$P/scratch/bin:$PATH"
export TMPDIR="$P/scratch/tmp"
