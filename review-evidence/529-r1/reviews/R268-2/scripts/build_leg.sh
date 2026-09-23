#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build one sim_nxn leg of tb/verilator/milan_dp from a disposable tree, with
# the Makefile's own variables (SHAPE_*, DP_VFLAGS / GPTP_OFF_VFLAGS, SRCS) and
# the per-leg recipes in legs.mk (copied from the `run` recipe).
#
# usage: build_leg.sh <tree> <leg> <mdir> [harness.cpp] [dp_src]
#   leg     nxn | nxndv | nxn8 | nxn4c | notify
#   harness path relative to tb/verilator/milan_dp (default sim_nxn.cpp); it
#           must live in that directory for its relative #includes
#   dp_src  path to a milan_datapath.sv copy (default: the tree's own)
# env: VERILATOR (the pinned 5.050 wrapper), JOBS (C++ build jobs, default 8)
set -eu
here=$(cd "$(dirname "$0")" && pwd)
tree=$1; leg=$2; mdir=$3; harness=${4:-sim_nxn.cpp}; dp=${5:-}
: "${VERILATOR:?set VERILATOR to the pinned 5.050}"
jobs=${JOBS:-8}
cd "$tree/tb/verilator/milan_dp"
set -- VERILATOR="$VERILATOR" VERILATOR_JOBS="$jobs" MDIR="$mdir" HARNESS="$harness"
[ -n "$dp" ] && set -- "$@" DP_SRC="$dp"
exec make -s --no-print-directory -f Makefile -f "$here/legs.mk" "review-$leg" "$@"
