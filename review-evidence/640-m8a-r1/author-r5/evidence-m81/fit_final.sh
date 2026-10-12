#!/usr/bin/env bash
# Scratch (M8a-1 evidence): the four points, split and flat, at the lane head; each unpiped, rc recorded.
set -u
L=$LANES/640-m8a
S=$VALIDATION_STORAGE/640m8a-a594/m81
O=$S/final-fit
R=$VALIDATION_STORAGE/640m8a-a594/fit2/runtime
export TMPDIR=$S/tmpdir MILAN_RV32_CC=$VALIDATION_STORAGE/502-a340-sdk/bin/riscv32-linux-gcc
mkdir -p "$O"
cd "$L" || exit 9
git rev-parse HEAD > "$O/head.txt"
git status --porcelain > "$O/status-before.txt"
for shape in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  for ifs in 1 2; do
    for layout in split flat; do
      n=$layout-$shape-if$ifs
      python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$shape.yaml --interfaces $ifs \
        --with-aecp --layout $layout --output "$O/$n" --libc "$R/libc.a" \
        --compiler-runtime "$R/libcompiler_rt.a" > "$O/$n.log" 2>&1
      echo $? > "$O/$n.rc"
    done
    stage=3344; [ $shape = endstation_ax7101_8x8 ] && stage=13264
    python3 sw/litex/ctrl_memory.py plan "$O/split-$shape-if$ifs/ctrl_app.elf" --stage-bytes $stage \
      > "$O/plan-$shape-if$ifs.json" 2> "$O/plan-$shape-if$ifs.err"
    echo $? > "$O/plan-$shape-if$ifs.rc"
  done
done
sha256sum "$O"/split-*/ctrl_app.elf "$S"/fit/split-*/ctrl_app.elf > "$O/elf.sha256"
git status --porcelain > "$O/status-after.txt"
echo done > "$O/done"
