#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Compile the three core objects with the base and the reviewed wire.h for RV32
# and count undefined __lshrdi3 references and text size per option set.
set -u
. "$(dirname "$0")/env.sh"
out=$SCRATCH/rv32sym; rm -rf "$out"; mkdir -p "$out/base/include" "$out/head/include"
git -C "$CLONE" show 70936b77:include/wire.h > "$out/base/include/wire.h"
git -C "$CLONE" show c687810b74b53b69c1fbdff7bfd0ec9da94eaa78:include/wire.h > "$out/head/include/wire.h"
CC=riscv64-elf-gcc
builtin=$($CC -print-file-name=include)
$CC --version | head -1
for march in rv32i rv32im; do
  for opt in -O0 -O2 -Os -O3; do
    for side in base head; do
      refs=0; text=0
      for src in adp acmp maap; do
        obj=$out/$side/$src-$march$opt.o
        $CC -march=$march -mabi=ilp32 $opt -ffreestanding -fno-builtin -nostdinc -isystem "$builtin" \
          -DNDEBUG -I"$out/$side/include" -I"$CLONE/include" -I"$CLONE/examples/rv32/include" \
          -c "$CLONE/src/$src.c" -o "$obj" || { echo "BUILD FAILED $side $src $march $opt"; exit 1; }
        r=$(riscv64-elf-nm -u "$obj" | grep -c '__lshrdi3'); refs=$((refs + r))
        t=$(riscv64-elf-size "$obj" | awk 'NR==2{print $1}'); text=$((text + t))
      done
      echo "$side $march $opt text=$text lshrdi3_objects=$refs"
    done
  done
done
