#!/bin/bash
# Reviewer probe: plant bridge-level epoch-fence/acknowledgement defects in a
# copy of the RTL and run every shipped harness that instantiates the bridge
# (the duplex at the default-regression window and the source-level test).
# Usage: probe_bridge_mutants.sh <repo> <verilator> <out-dir> <name> <old> <new>
set -u
repo=$1; engine=$2; out=$3; name=$4; old=$5; new=$6
case_dir=$out/$name
mkdir -p "$case_dir/rtl"
cp "$repo"/hdl/milan/usbaudio/*.sv "$case_dir/rtl/"
if [ "$name" != baseline ]; then
  python3 -I - "$case_dir/rtl/KL_usbaudio_bridge.sv" "$old" "$new" <<'PY'
import sys
path, old, new = sys.argv[1:4]
text = open(path).read()
if text.count(old) != 1:
    sys.exit("plant must match exactly once")
open(path, "w").write(text.replace(old, new))
PY
  [ $? -eq 0 ] || { echo "$name PLANT_FAILED"; exit 2; }
fi
fifo=$repo/third_party/verilog-axis/rtl/axis_async_fifo.v
tb=$repo/tb/verilator/usbaudio
"$engine" --cc --exe --build --top-module KL_usbaudio_bridge -Wno-fatal -Wno-lint -Wno-style \
  --build-jobs 4 -GWINDOW_LOG2_P=5 -CFLAGS "-O2 -std=c++17 -DWINDOW_LOG2_TB=5" \
  --Mdir "$case_dir/duplex" "$case_dir"/rtl/*.sv "$fifo" "$tb/duplex.cpp" > "$case_dir/duplex-build.log" 2>&1
d_build=$?
"$engine" --binary --timing --top-module levels_tb -Wno-fatal -Wno-lint -Wno-style --build-jobs 4 \
  --Mdir "$case_dir/levels" "$case_dir"/rtl/*.sv "$fifo" "$tb/levels_tb.sv" > "$case_dir/levels-build.log" 2>&1
l_build=$?
d_run=build_failed; l_run=build_failed
if [ $d_build -eq 0 ]; then "$case_dir/duplex/VKL_usbaudio_bridge" 1000 > "$case_dir/duplex.log" 2>&1; d_run=$?; fi
if [ $l_build -eq 0 ]; then "$case_dir/levels/Vlevels_tb" > "$case_dir/levels.log" 2>&1; l_run=$?; fi
echo "$name duplex_rc=$d_run levels_rc=$l_run duplex_check=$(grep -o 'CHECK [A-Z_]*' "$case_dir/duplex.log" | head -1) levels_check=$(grep -o 'CHECK [A-Z_]*' "$case_dir/levels.log" | head -1)"
