#!/bin/sh
# Link the split control firmware at the four fit points of one source tree
# and plan each image with that tree's own ctrl_memory.py.
# usage: link_points.sh <tree> <out> <python> <runtime-dir>
# Needs MILAN_RV32_CC (the pinned RV32 SDK compiler) in the environment.
set -u
tree=$1 out=$2 py=$3 rt=$4
mkdir -p "$out"
for point in "1x1_tdm8 1 3344" "1x1_tdm8 2 3344" "8x8 1 13264" "8x8 2 13264"; do
  set -- $point
  for layout in split flat; do
    tag=${1}_i${2}_${layout}
    (
      cd "$tree" || exit 9
      "$py" sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/endstation_ax7101_$1.yaml" \
        --interfaces "$2" --with-aecp --layout "$layout" --output "$out/$tag" \
        --libc "$rt/libc.a" --compiler-runtime "$rt/libcompiler_rt.a" > "$out/$tag.log" 2>&1
      echo $? > "$out/$tag.rc"
      if [ "$layout" = split ]; then
        "$py" sw/litex/ctrl_memory.py plan "$out/$tag/ctrl_app.elf" --stage-bytes "$3" \
          > "$out/$tag.plan" 2>&1
        echo $? > "$out/$tag.plan.rc"
      fi
    ) &
  done
done
wait
