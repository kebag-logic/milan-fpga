#!/bin/bash
# Usage: run_boundary.sh <repo> <packet> <sdk-gcc>: the 697c boundary gate over the Verilator builders (it captures
# the MAAP differential), as the hosted firmware-verilator job runs it. PATH must give pinned verilator and clang-18.
set -u; R=$1; P=$2; L=$P/logs/boundary-verilator
mkdir -p "$P/scratch/tmp/boundary"; export TMPDIR=$P/scratch/tmp/boundary MILAN_RV32_CC=$3
export PKG_CONFIG_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$VALIDATION_TOOLS/gtest-1.14.0 LD_LIBRARY_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib
cd "$R" || exit 9
{ echo "head=$(git rev-parse HEAD) verilator=$(verilator --version) clang=$(clang --version | head -1) rv32=$MILAN_RV32_CC start=$(date -Is)"
  python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator; rc=$?
  echo "end=$(date -Is) rc=$rc"; exit $rc; } > "$L.log" 2>&1
echo $? > "$L.rc"
