#!/bin/bash
# Link the size fixture's image (the CPU budget harness's arm A image, .text identical) of TREE at 1x1/1if and
# 8x8/2if, and print declare_sources's size and the hot functions after it (lane 895 round 2).
# usage: trial.sh TREE TAG
set -u
TREE=$1 TAG=$2 R=/data-2/milan/tmp/665s2b-a683zm/builds O=/data-2/milan/tmp/895-a775/r2/trial
. $MANAGEMENT/2026-09-23/895-a775/scripts/env.sh
mkdir -p $O
for spec in "1x1 endstation_ax7101_1x1_tdm8 1 GA1" "8x8 endstation_ax7101_8x8 2 GA8"; do
  set -- $spec; fx=(); [ $1 = 8x8 ] && fx=(--ledgered-point 8x8-two-interfaces)
  rm -rf $O/$TAG-$1
  ( cd $TREE && python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$2.yaml --interfaces $3 --with-aecp \
      --layout split "${fx[@]}" --output $O/$TAG-$1 --flash-map $R/$4/split-soc/flash-map --libc $R/$4/runtime/libc.a \
      --compiler-runtime $R/$4/runtime/libcompiler_rt.a ) > $O/$TAG-$1.log 2>&1 || { echo "$TAG $1 rc $?"; continue; }
  e=$(ls $O/$TAG-$1/*.elf | head -1)
  echo "$TAG $1: $(riscv32-buildroot-linux-gnu-nm -S -n $e | grep -E ' (declare_sources|mrp_attr_visit|_ctrl_hot_end)$' | awk '{print $NF"="$1"/"$2}' | tr '\n' ' ')"
done
