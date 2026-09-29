# source me from anywhere: GNU make 4.3 (built from the upstream make-4.3.tar.gz,
# sha256 e05fdde47c5f7ca45cb697e973894ff4f5d79e13b750ed57d7b66d8defc78e19) and the
# -j-capped pinned Verilator 5.050 first on PATH; temp dirs in scratch.
P=${P:-$REVIEWS/617-r395-4-packet}
export REAL_VERILATOR=${REAL_VERILATOR:-$VALIDATION_TOOLS/verilator-v5.050-src/bin/verilator}
export PATH="$P/scratch/bin43:$PATH"
export TMPDIR="$P/scratch/tmp"
unset MAKEFLAGS MFLAGS MAKELEVEL
