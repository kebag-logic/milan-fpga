#!/bin/sh
# Head harnesses (media_grid_align, chmap_capture main legs) against BASE RTL.
#   base_rtl_head_harness.sh <head_tree> <base_tree> <scratch_dir> <out_file>
set -eu
HEAD=$1; BASE=$2; S=$3; OUT=$4
V=${VERILATOR:-verilator}
rm -rf "$S"; mkdir -p "$S"
cp -r "$BASE/hdl" "$S/"; cp -r "$HEAD/tb" "$S/"
# never reuse a build product copied from another tree
find "$S/tb" -maxdepth 3 -type d -name 'obj_*' -prune -exec rm -rf {} +
( cd "$S/tb/verilator/media_grid_align" &&
  "$V" --cc --exe --build -j 4 --top-module media_grid_align_wrap -Wno-fatal -Wno-lint -Wno-style \
    -Wno-PINCONNECTEMPTY +incdir+../../../hdl/common -CFLAGS "-std=c++17 -O2 -I$PWD" \
    media_grid_align_wrap.sv ../../../hdl/ieee1722/crf/KL_media_grid_align.sv \
    ../../../hdl/ieee1722/crf/KL_media_nco.sv ../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv \
    sim_main.cpp -o Vmedia_grid_align_sim > build.log 2>&1 &&
  { ./obj_dir/Vmedia_grid_align_sim > run.log 2>&1 || true; } ) &
( cd "$S/tb/verilator/chmap_capture" && make VERILATOR="$V" obj_dir/Vchmap_wrap > build.log 2>&1 &&
  { ./obj_dir/Vchmap_wrap > run.log 2>&1 || true; } ) &
wait
{
  echo "== base RTL + head harnesses =="
  grep -E 'checks, [0-9]+ failures' "$S/tb/verilator/media_grid_align/run.log"
  grep -E '\[FAIL\]|window|acquisition' "$S/tb/verilator/media_grid_align/run.log"
  grep -E 'checks, [0-9]+ failures' "$S/tb/verilator/chmap_capture/run.log"
  grep '\[FAIL\]' "$S/tb/verilator/chmap_capture/run.log"
} > "$OUT"
cat "$OUT"
