#!/bin/sh
# Build the junction-law probe.   build.sh <head_tree> <base_tree> <out_dir>
set -eu
HEAD_TREE=$1; BASE_TREE=$2; OUT=$3
HERE=$(cd "$(dirname "$0")" && pwd)
V=${VERILATOR:-verilator}
mkdir -p "$OUT"
sed 's/^module KL_chan_map_capture #(/module KL_chan_map_capture_base #(/' \
  "$BASE_TREE"/hdl/ieee1722/aaf/KL_chan_map_capture.sv > "$OUT"/KL_chan_map_capture_base.sv
test "$(diff "$BASE_TREE"/hdl/ieee1722/aaf/KL_chan_map_capture.sv "$OUT"/KL_chan_map_capture_base.sv | grep -c '^[<>]')" = 2
"$V" --cc --exe --build -j 4 --top-module law_wrap -Wno-fatal -Wno-lint -Wno-style -Wno-PINCONNECTEMPTY \
  +incdir+"$HEAD_TREE"/hdl/common -CFLAGS "-std=c++17 -O2" --Mdir "$OUT" \
  "$HERE"/law_wrap.sv "$HEAD_TREE"/hdl/ieee1722/aaf/KL_chan_map_capture.sv \
  "$OUT"/KL_chan_map_capture_base.sv "$HERE"/law.cpp -o law > "$OUT"/build.log 2>&1
echo "built $OUT/law"
