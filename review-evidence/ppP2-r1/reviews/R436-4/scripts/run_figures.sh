#!/usr/bin/env bash
# run_figures.sh : the exact head's tb/nvm_port figures gate (measure_figures.py --check)
# in an extraction, each Verilator build at -j 4 instead of -j 0.
set -u
P=$(cd "$(dirname "$0")/.." && pwd)
HEAD=3957814550f164d72bfaad5d28cd0e7cac0ecaaf
d=$P/scratch/figures; rm -rf "$d"; mkdir -p "$d"
git -C $REVIEWS/r436-4-ppP2 archive "$HEAD" hdl/packet_engine tb/nvm_port tb/common | tar -x -C "$d"
sed -i 's/--build -j 0/--build -j 4/' "$d/tb/nvm_port/Makefile"
cd "$d/tb/nvm_port"
export TMPDIR=$P/scratch/figures_tmp; mkdir -p "$TMPDIR"
/usr/bin/time -f "wall %e s, maxrss %M KB" python3 measure_figures.py --check
