#!/bin/bash
# usage: run.sh NAME COMMIT [LANE]  -> builds release (rv32i -O3) and split (rv32im -Os) harnesses and runs them
set -e
S=$VALIDATION_STORAGE/tsn26-a750c
name=$1; commit=$2; lane=$3
tree=$S/measure/tree-$name
rm -rf $tree; mkdir -p $tree
git -C $LANES/tsn-c-stack-26-owed archive $commit | tar -x -C $tree
for cfg in release:rv32i:-O3 split:rv32im:-Os; do
  IFS=: read k isa opt <<< "$cfg"
  out=$S/measure/$name-$k
  rm -rf $out
  $S/measure/build.sh $tree $out $isa $opt $lane
  timeout 60 qemu-system-riscv32 -machine virt -nographic -bios none -icount shift=0 -kernel $out/measure.elf -no-reboot > $out/result.txt 2>&1 || true
  sha256sum $out/measure.elf | cut -d' ' -f1 > $out/elf.sha256
done
