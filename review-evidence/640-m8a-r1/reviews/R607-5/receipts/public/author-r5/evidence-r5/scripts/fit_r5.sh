#!/usr/bin/env bash
# Scratch (M8a-1 round 5): the four points, split and flat, in one tree; each unpiped, rc recorded.
# usage: fit_r5.sh <tree> <out>
set -u
T=$1
O=$2
R=$VALIDATION_STORAGE/640m8a-a594/r5/runtime
export TMPDIR=$VALIDATION_STORAGE/640m8a-a594/r5/tmp MILAN_RV32_CC=$VALIDATION_STORAGE/502-a340-sdk/bin/riscv32-linux-gcc PYTHONDONTWRITEBYTECODE=1
mkdir -p "$O"
cd "$T" || exit 9
git rev-parse HEAD > "$O/head.txt"
git status --porcelain > "$O/status-before.txt"
sha256sum "$R/libc.a" "$R/libcompiler_rt.a" > "$O/runtime.sha256"
for shape in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  for ifs in 1 2; do
    for layout in split flat; do
      n=$layout-$shape-if$ifs
      python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$shape.yaml --interfaces $ifs \
        --with-aecp --layout $layout --output "$O/$n" --libc "$R/libc.a" \
        --compiler-runtime "$R/libcompiler_rt.a" > "$O/$n.log" 2>&1
      echo $? > "$O/$n.rc"
    done &
  done
done
wait
for shape in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  for ifs in 1 2; do
    stage=3344; [ $shape = endstation_ax7101_8x8 ] && stage=13264
    python3 sw/litex/ctrl_memory.py plan "$O/split-$shape-if$ifs/ctrl_app.elf" --stage-bytes $stage \
      > "$O/plan-$shape-if$ifs.json" 2> "$O/plan-$shape-if$ifs.err"
    echo $? > "$O/plan-$shape-if$ifs.rc"
  done
done
sha256sum "$O"/split-*/ctrl_app.elf "$O"/flat-*/ctrl_app.elf > "$O/elf.sha256"
git status --porcelain > "$O/status-after.txt"
echo done > "$O/done"
