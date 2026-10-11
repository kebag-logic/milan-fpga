#!/bin/bash
# Reproduce this packet's executable evidence.
# Usage: run_review.sh <clone at f5d0fb0e> <packet dir> <pinned verilator 5.050 wrapper>
# The clone must have gptp-processor, protocol-processor and
# third_party/verilog-axis checked out at their gitlinks. A disposable copy of
# the clone is made for milan_dp, because milan_dp_gm_steps builds in
# tb/verilator/milan_dp too and the two must not share a tree concurrently.
set -u
clone=$1; packet=$2; vl=$3
mkdir -p "$packet/scratch/bin" "$packet/receipts"
ln -sf "$vl" "$packet/scratch/bin/verilator"
cp -a "$clone" "$packet/scratch/tree_dp"
run="$packet/scripts/run_logged.sh"
"$run" gm_steps_suite "$clone" make -C tb/verilator/milan_dp_gm_steps VERILATOR_JOBS=6 &
"$run" gptp_plane_suite "$clone" make -C tb/verilator/gptp_plane &
"$run" milan_dp_suite "$packet/scratch/tree_dp" make -C tb/verilator/milan_dp VERILATOR_JOBS=4 &
wait
# Short leg against the full leg; needs the obj_gmstep the suite built.
"$packet/scripts/probe_short_leg.sh" "$clone/tb/verilator/milan_dp" \
  "$packet/receipts/gm_steps_suite.log" "$packet/scratch/short_leg"
# Base donor generator through the head regression (issue item 1).
mkdir -p "$packet/scratch/basegen"
git -C "$clone/gptp-processor" show \
  5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d:hdl/ucode/gen_gptp_ucode.py \
  > "$packet/scratch/basegen/gen_gptp_ucode.py"
(cd "$clone" && PATH="$packet/scratch/bin:$PATH" VERILATOR_JOBS=8 \
  python3 tb/verilator/gptp_plane/phc_step.py --work "$packet/scratch/phc_base" \
  --generator "$packet/scratch/basegen/gen_gptp_ucode.py")
echo "base-generator regression rc=$? (1 required)"
# Shard ownership.
(cd "$clone" && python3 scripts/suite_shards.py --selftest &&
  for s in 0 1 2 3 4; do
    python3 scripts/suite_shards.py --suite-root tb/verilator --shard "$s/5"; done)
