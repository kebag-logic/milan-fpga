#!/bin/sh
# Reproduce R485-1's three physical-leg runs from a clean checkout of
# d0e29f6dda6f04f3ace1dbb395f57379e58cacaf (submodules initialised).
# Usage: run_controls.sh <clean-checkout> <work-dir> <dir-containing-verilator-5.050>
# Each copy runs `make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4`
# concurrently; logs and rc files land in <work-dir>.
set -eu
SRC=$1; WORK=$2; VDIR=$3
mkdir -p "$WORK"
for d in head c1 c2; do rsync -a "$SRC"/ "$WORK/$d"/; rm -rf "$WORK/$d/tb/verilator/milan_dp/obj_ax1x1gptp"; done
# C1: #629's A2-a removed (the existing tdm8render mutant line), new pacing kept
sed -i 's/^  wire        mga_sel_w = int_clk_selected_r | follow_sel_r;$/  wire        mga_sel_w = follow_sel_r;/' \
  "$WORK/c1/hdl/milan/milan_datapath.sv"
grep -q '^  wire        mga_sel_w = follow_sel_r;$' "$WORK/c1/hdl/milan/milan_datapath.sv"
# C2: the parent's harness (old axis-clock pacing) on the head's RTL
git -C "$SRC" show c0280fc008ef9c5c1650402a58bab3e47a92127b:tb/verilator/milan_dp/sim_ax1x1gptp.cpp \
  > "$WORK/c2/tb/verilator/milan_dp/sim_ax1x1gptp.cpp"
for d in head c1 c2; do
  ( cd "$WORK/$d" && PATH="$VDIR:$PATH" make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4 \
      > "$WORK/run.$d.log" 2>&1; echo $? > "$WORK/run.$d.rc" ) &
done
wait
grep -H "checks: .* failures" "$WORK"/run.*.log
