#!/bin/sh
# Build the base-vs-head lockstep probe.
#   build.sh <head_tree> <base_tree> <out_dir>
# The base KL_media_grid_align is copied with ONLY its module name changed
# (the copy is refused if the rename did not happen exactly once).
set -eu
HEAD_TREE=$1; BASE_TREE=$2; OUT=$3
HERE=$(cd "$(dirname "$0")" && pwd)
V=${VERILATOR:-verilator}
mkdir -p "$OUT"
sed 's/^module KL_media_grid_align #(/module KL_media_grid_align_base #(/' \
  "$BASE_TREE"/hdl/ieee1722/crf/KL_media_grid_align.sv > "$OUT"/KL_media_grid_align_base.sv
test "$(grep -c '^module KL_media_grid_align_base #(' "$OUT"/KL_media_grid_align_base.sv)" = 1
test "$(diff "$BASE_TREE"/hdl/ieee1722/crf/KL_media_grid_align.sv "$OUT"/KL_media_grid_align_base.sv | grep -c '^[<>]')" = 2
"$V" --cc --exe --build -j 4 --top-module equiv_wrap -Wno-fatal -Wno-lint -Wno-style \
  -CFLAGS "-std=c++17 -O2" --Mdir "$OUT" \
  "$HERE"/equiv_wrap.sv \
  "$HEAD_TREE"/hdl/ieee1722/crf/KL_media_grid_align.sv \
  "$OUT"/KL_media_grid_align_base.sv \
  "$HEAD_TREE"/hdl/ieee1722/crf/KL_media_nco.sv \
  "$HERE"/equiv.cpp -o equiv > "$OUT"/build.log 2>&1
echo "built $OUT/equiv"
