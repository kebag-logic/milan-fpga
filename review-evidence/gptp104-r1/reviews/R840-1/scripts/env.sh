# Source me: the probe environment. Pinned Verilator first on PATH, temporary
# files and every ccache directory under the packet's scratch tree.
P=$REVIEWS/gptp104-r840-1-packet
S=$P/scratch
export PATH=$S/bin:$PATH TMPDIR=$S/tmp
unset OBJCACHE CCACHE_BASEDIR CCACHE_NOHASHDIR
