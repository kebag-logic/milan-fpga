#!/bin/sh
# Reviewer probes for PR #631 at a463a1deb9d63614e8bd2134ccd7b2cd541c72ed (R428-3).
# Usage: run_probes.sh <clone at the head> <scratch dir> <pinned HDL simulator>
# Every probe drives the unmodified hdl/ieee1722/avtp/KL_media_clock_restart.sv.
set -e
CLONE=$1; S=$2; V=$3; P=$(cd "$(dirname "$0")" && pwd)
RTL="$CLONE/hdl/ieee1722/avtp/KL_media_clock_restart.sv"
build() { # <dir> <cpp> <exe>
  mkdir -p "$S/$1"; cp "$2" "$S/$1/"; (cd "$S/$1" && "$V" --cc --exe --build -O3 -j 8 \
    -Wno-fatal --top-module KL_media_clock_restart -GN_TALKERS_P=2 "$RTL" \
    "$(basename "$2")" -o "$3" > build.log 2>&1)
}
# 1. the author's round-3 switch harness, the six published case lines
build switch "$P/mcr_switch_rerun/sim_switch.cpp" sim_switch
i=0; while read -r args; do i=$((i+1)); "$S/switch/obj_dir/sim_switch" $args > "$S/switch/out.$i" & done < "$P/mcr_switch_rerun/cases.txt"; wait
cat "$S"/switch/out.1 "$S"/switch/out.2 "$S"/switch/out.3 "$S"/switch/out.4 "$S"/switch/out.5 "$S"/switch/out.6 > "$P/mcr_switch_rerun/receipt_author_cases.out"
# 2. the reviewer's round-2 merge probe, unchanged
build r2 "$P/mcr_merge_probe_r2_rerun/sim_main.cpp" sim_main
"$S/r2/obj_dir/sim_main" > "$P/mcr_merge_probe_r2_rerun/receipt.out"; echo $? > "$P/mcr_merge_probe_r2_rerun/receipt.rc"
# 3. the reviewer's merge-window sweep: A LAT OFF phase_step d_step d_max
build win "$P/mcr_window_probe/sim_window.cpp" sim_window
W="$S/win/obj_dir/sim_window"
( "$W" 100 40 53 53 11 3200 > "$P/mcr_window_probe/w1.out"; echo $? > "$P/mcr_window_probe/w1.rc" ) &
( "$W" 100 90 1201 47 13 3400 > "$P/mcr_window_probe/w2.out"; echo $? > "$P/mcr_window_probe/w2.rc" ) &
( "$W" 64 40 7 29 5 2100 > "$P/mcr_window_probe/w3.out"; echo $? > "$P/mcr_window_probe/w3.rc" ) &
( "$W" 100 2 0 1 97 3300 > "$P/mcr_window_probe/w4.out"; echo $? > "$P/mcr_window_probe/w4.rc" ) &
wait
# 4. the ring area probe (xc7 mapping, flattened)
cd "$P/ring_area_probe"
yosys -q -p "read_verilog -sv ring_probe.sv; chparam -set DEPTH 8 -set SHIFT 3 -set SPAN 32'd4096000000 ring_probe; synth_xilinx -family xc7 -top ring_probe -flatten; tee -o stat_e8.txt stat"
yosys -q -p "read_verilog -sv ring_probe.sv; chparam -set DEPTH 256 -set SHIFT 0 -set SPAN 32'd512000000 ring_probe; synth_xilinx -family xc7 -top ring_probe -flatten; tee -o stat_e1.txt stat"
yosys -q -p "read_verilog -sv ring_probe_async.sv; synth_xilinx -family xc7 -top ring_probe_async -flatten; tee -o stat_e8_async.txt stat"
# 5. desk checks (standard library only)
cd "$P"
python3 -I loop_gain_check.py > loop_gain_check.out; echo $? > loop_gain_check.rc
python3 -I e8_meter_probe.py all > e8_meter_probe.out; echo $? > e8_meter_probe.rc
