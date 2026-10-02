# Common environment for the review runs: pinned Verilator first on PATH,
# private copies under the packet's scratch TMPDIR (not the tmpfs /tmp, which
# would be charged to the memory cap).
P=$REVIEWS/pp143-r440-1-packet
SRC=$REVIEWS/r440-1-pp143
export PATH=$P/scratch/bin:$PATH
export TMPDIR=$P/scratch/tmp
