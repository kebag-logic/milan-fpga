#!/usr/bin/env bash
# fuzz_extra.sh MAXP TMO... : the exact head's standing randomized harness (`make fuzz`)
# at extra legal bounds, built at MAX_PAYLOAD_P = MAXP, in its own extraction.
set -u
P=$(cd "$(dirname "$0")/.." && pwd)
m=$1; shift
d=$P/scratch/fuzz_extra_$m; rm -rf "$d"; mkdir -p "$d"
git -C $REVIEWS/r436-4-ppP2 archive 3957814550f164d72bfaad5d28cd0e7cac0ecaaf hdl/packet_engine tb/nvm_port tb/common | tar -x -C "$d"
sed -i 's/--build -j 0/--build -j 2/' "$d/tb/nvm_port/Makefile"
cd "$d/tb/nvm_port"
make -k fuzz FUZZ_TMOS="$*" FUZZ_MAXP=$m VERILATOR=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator} > make.log 2>&1
echo "rc=$?"
grep -E '^(fuzz:|[0-9]+ checks:|FAIL)' make.log | cut -c1-300
