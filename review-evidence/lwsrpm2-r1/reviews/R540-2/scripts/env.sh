# Source from the packet root: PKT is the packet, SRC the exact-head clone.
PKT=${PKT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
SRC=${SRC:-$REVIEWS/r540-2-lwsrpm2}
export CGREEN_PREFIX=$PKT/scratch/cgreen
export CMAKE_PREFIX_PATH=$CGREEN_PREFIX
export LD_LIBRARY_PATH=$CGREEN_PREFIX/lib
export CPATH=$CGREEN_PREFIX/include
export LIBRARY_PATH=$CGREEN_PREFIX/lib
