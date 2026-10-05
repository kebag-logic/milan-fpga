#!/bin/sh
# R484-1: reproduce runs H / C1 / C2 concurrently from a clean clone at
# d0e29f6dda6f04f3ace1dbb395f57379e58cacaf (submodules at their gitlinks).
# Usage: sh run_controls.sh <clean clone> <scratch dir> <pinned verilator dir>
set -eu
SRC=$1; S=$2; VDIR=$3
mkdir -p "$S"
for v in H C1 C2; do rm -rf "$S/$v"; cp -a "$SRC" "$S/$v"; done
# C1: A2-a removed (the PR's own planted line), fixed bench
sed -i 's/^  wire        mga_sel_w = int_clk_selected_r | follow_sel_r;$/  wire        mga_sel_w = follow_sel_r;/' "$S/C1/hdl/milan/milan_datapath.sv"
# C2: head RTL with the parent's axis-paced harness
git -C "$S/C2" show c0280fc008ef9c5c1650402a58bab3e47a92127b:tb/verilator/milan_dp/sim_ax1x1gptp.cpp \
  > "$S/C2/tb/verilator/milan_dp/sim_ax1x1gptp.cpp"
for v in H C1 C2; do
  ( cd "$S/$v" && PATH="$VDIR:$PATH" sh -c "verilator --version > '$S/$v.log';
      /usr/bin/time -f 'driver_wall=%e' make -j4 -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4 >> '$S/$v.log' 2>&1;
      echo \$? > '$S/$v.rc'" ) &
done
wait
for v in H C1 C2; do echo "$v make rc $(cat "$S/$v.rc")"; done
