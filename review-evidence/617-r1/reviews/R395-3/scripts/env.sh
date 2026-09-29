# source me: pinned simulator first on PATH, 4-job build cap per stream, temp dirs in scratch
P=$REVIEWS/617-r395-3-packet
export REAL_VERILATOR=$VALIDATION_TOOLS/verilator-v5.050-src/bin/verilator
export PATH="$P/scratch/bin:$PATH"
export TMPDIR="$P/scratch/tmp"
