#!/bin/sh
# usage: run_lv_probe.sh <exported-head-tree> <work-dir> <verilator>
# Builds tb/srp_stream_fsms with its main() replaced by lv_probe_tail.cpp.
set -e
HEAD=$1; W=$2; V=$3; HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$W"; mkdir -p "$W"; cp -r "$HEAD/hdl" "$W/"; mkdir -p "$W/tb"; cp -r "$HEAD/tb/srp_stream_fsms" "$HEAD/tb/common" "$W/tb/"
cd "$W/tb/srp_stream_fsms"
n=$(grep -n '^int main' sim_main.cpp | cut -d: -f1)
head -n $((n-1)) sim_main.cpp > probe_main.cpp
cat "$HERE/lv_probe_tail.cpp" >> probe_main.cpp
make run VERILATOR="$V" CPP=probe_main.cpp
