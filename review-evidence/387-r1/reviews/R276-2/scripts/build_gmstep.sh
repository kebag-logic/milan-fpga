#!/bin/sh
# Build the milan_dp gmstep leg through the tree's own recipe into an
# out-of-tree object directory, optionally against mutated copies of the
# datapath, the render setpoint stage or the clock-validity block.
# Usage: build_gmstep.sh <clone> <verilator> <mdir> [DP_SRC=..] [RSP_SRC=..] [CLKV_SRC=..]
set -eu
repo=$1; ver=$2; mdir=$3; shift 3
cd "$repo/tb/verilator/milan_dp"
exec make gmstep-build VERILATOR="$ver" VERILATOR_JOBS="${VJOBS:-2}" GMSTEP_MDIR="$mdir" "$@"
