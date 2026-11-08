#!/bin/bash
# usage: run.sh TREE  -> prints symbol sizes on x86-64 (gcc) and RV32 (riscv64-elf-gcc ilp32)
S=$VALIDATION_STORAGE/tsn26-a750d; T=$1
inc=$(riscv64-elf-gcc -print-file-name=include)
gcc -std=c11 -I$T/include -c $S/sizes/sizes.c -o $S/sizes/x86.o && echo x86-64: $(nm -S --size-sort -t d $S/sizes/x86.o | awk '{print $4"="$2+0}')
riscv64-elf-gcc -march=rv32i -mabi=ilp32 -ffreestanding -nostdinc -isystem $inc -std=c11 -I$T/include -I$T/examples/rv32/include -c $S/sizes/sizes.c -o $S/sizes/rv32.o && echo rv32: $(riscv64-elf-nm -S --size-sort -t d $S/sizes/rv32.o | awk '{print $4"="$2+0}')
