#!/bin/bash
# usage: sizes.sh TREE OUTDIR  -- prints struct sizes for x86-64 and RV32 (ilp32)
set -eu
tree=$1; out=$2; here=$(cd "$(dirname "$0")" && pwd); mkdir -p "$out"
inc=$(riscv64-elf-gcc -print-file-name=include)
gcc -std=c11 -c -I"$tree/include" "$here/sizes.c" -o "$out/x86.o"
riscv64-elf-gcc -march=rv32i -mabi=ilp32 -ffreestanding -nostdinc -isystem "$inc" -std=c11 -c -I"$tree/include" -I"$tree/examples/rv32/include" "$here/sizes.c" -o "$out/rv32.o"
for t in x86 rv32; do nm -S --size-sort "$out/$t.o" | awk -v t=$t '{printf "%s %s %d\n", t, $4, strtonum("0x"$2)}'; done
