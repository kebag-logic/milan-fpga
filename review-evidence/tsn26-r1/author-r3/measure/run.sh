#!/bin/bash
# usage: run.sh NAME TREE MEASURE_C [LANE]  -> builds release (rv32i -O3) and split (rv32im -Os) harnesses and runs them
set -e
S=$VALIDATION_STORAGE/tsn26-a750d
name=$1; tree=$2; export MEASURE_C=$3; lane=${4:-}
for cfg in release:rv32i:-O3 split:rv32im:-Os; do
  IFS=: read k isa opt <<< "$cfg"
  out=$S/measure/$name-$k
  rm -rf $out
  $S/measure/build.sh $tree $out $isa $opt $lane
  timeout 60 qemu-system-riscv32 -machine virt -nographic -bios none -icount shift=0 -kernel $out/measure.elf -no-reboot > $out/result.txt 2>&1 || true
  sha256sum $out/measure.elf | cut -d' ' -f1 > $out/elf.sha256
done
