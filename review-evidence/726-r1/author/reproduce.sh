#!/bin/sh
set -eu
: "${REPO_ROOT:?Set the repository checkout}"
: "${SCRATCH:?Set a disk scratch directory}"
: "${PINNED_VERILATOR:?Set the pinned compiler executable}"
EVIDENCE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mkdir -p "$SCRATCH"
for count in 2 9; do
  timeout 570s env VERILATOR_JOBS=2 "$PINNED_VERILATOR" \
    --cc --exe --build -j 8 --top-module KL_aecp_notify \
    -GN_CTRL_P=2 -GN_STREAM_IN_P="$count" -GN_STREAM_OUT_P="$count" \
    -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
    -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
    -CFLAGS "-std=c++17 -O2 -DSTREAMS=$count" \
    --Mdir "$SCRATCH/obj_$count" \
    "$REPO_ROOT/protocol-processor/hdl/common/pp_pkg.sv" \
    "$REPO_ROOT/protocol-processor/hdl/aecp/KL_aecp_notify.sv" \
    "$EVIDENCE_DIR/cadence.cpp" -o cadence \
    > "$SCRATCH/build_$count.log" 2>&1
  timeout 570s "$SCRATCH/obj_$count/cadence" > "$SCRATCH/cadence_$count.csv"
done
