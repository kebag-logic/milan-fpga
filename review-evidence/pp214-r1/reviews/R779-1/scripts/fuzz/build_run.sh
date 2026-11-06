#!/bin/bash
# usage: build_run.sh <tree> <depth> <tag> <seeds> <cycles> [density]
# Builds the encoder alone from <tree> and runs the seeds; prints one line per seed.
PKT=${PKT:-$(cd "$(dirname "$0")/../.." && pwd)}
export PATH=${VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}:$PATH
t=$1; depth=$2; tag=$3; seeds=$4; cyc=$5; dens=${6:-3}
o=$PKT/scratch/fuzz/$tag; mkdir -p "$o"
verilator --cc --exe --build -j 2 --top-module KL_srp_encoder -GDEPTH_P=$depth -Wno-fatal -Wno-lint --Mdir "$o" \
  -CFLAGS "-std=c++17 -O2" "$t/hdl/common/pp_pkg.sv" "$t/hdl/srp/KL_srp_encoder.sv" "$PKT/scripts/fuzz/enc_fuzz.cpp" -o fz > "$o/build.log" 2>&1 || { echo "$tag BUILD FAILED"; tail -5 "$o/build.log"; exit 3; }
rc=0
for s in $seeds; do "$o/fz" "$s" "$cyc" "$dens" | tail -12 || rc=1; [ "${PIPESTATUS[0]}" = 0 ] || rc=1; done
echo "$tag rc=$rc"; exit $rc
