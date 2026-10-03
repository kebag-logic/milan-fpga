#!/usr/bin/env bash
# run_head.sh : extract the exact head's port, suite and harness and run `make run`
# (elab_bounds.sh, suite at 100/37/20, randomized harness at 1/2/3/37) at -j 2.
set -u
P=$(cd "$(dirname "$0")/.." && pwd)
HEAD=3957814550f164d72bfaad5d28cd0e7cac0ecaaf
d=$P/scratch/head; rm -rf "$d"; mkdir -p "$d"
git -C $REVIEWS/r436-4-ppP2 archive "$HEAD" hdl/packet_engine tb/nvm_port tb/common | tar -x -C "$d"
sed -i 's/--build -j 0/--build -j 2/' "$d/tb/nvm_port/Makefile"
cd "$d/tb/nvm_port"
/usr/bin/time -f "wall %e s, maxrss %M KB" make -k run VERILATOR=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator} > make.log 2>&1
rc=$?
echo "== head rc=$rc"
grep -E '^(fuzz:|[0-9]+ checks:|FAIL|wall)' make.log | cut -c1-400
