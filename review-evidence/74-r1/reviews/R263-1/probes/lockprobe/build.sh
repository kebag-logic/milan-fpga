#!/bin/sh
# Build the raced-lock probe against one RTL tree.
#   build.sh <wrap_tree> <rtl_tree> <out_dir> [extra verilator args...]
# <wrap_tree>: tree whose tb/verilator/media_grid_align/media_grid_align_wrap.sv is used
# <rtl_tree> : tree whose hdl/ supplies KL_media_grid_align, KL_media_nco, KL_chan_map_capture
# VERILATOR (env) selects the binary; the reviewer used the pinned 5.050.
set -eu
WRAP_TREE=$1; RTL_TREE=$2; OUT=$3; shift 3
HERE=$(cd "$(dirname "$0")" && pwd)
V=${VERILATOR:-verilator}
mkdir -p "$OUT"
"$V" --cc --exe --build -j 4 --top-module media_grid_align_wrap \
  -Wno-fatal -Wno-lint -Wno-style -Wno-PINCONNECTEMPTY \
  +incdir+"$RTL_TREE"/hdl/common \
  -CFLAGS "-std=c++17 -O2" --Mdir "$OUT" "$@" \
  "$WRAP_TREE"/tb/verilator/media_grid_align/media_grid_align_wrap.sv \
  "$RTL_TREE"/hdl/ieee1722/crf/KL_media_grid_align.sv \
  "$RTL_TREE"/hdl/ieee1722/crf/KL_media_nco.sv \
  "$RTL_TREE"/hdl/ieee1722/aaf/KL_chan_map_capture.sv \
  "$HERE"/lockprobe.cpp -o lockprobe > "$OUT"/build.log 2>&1
echo "built $OUT/lockprobe"
