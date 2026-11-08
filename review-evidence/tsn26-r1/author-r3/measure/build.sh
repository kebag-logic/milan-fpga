#!/bin/bash
# usage: build.sh TREE OUT ISA OPT [extra cflags]
set -e
tree=$1; out=$2; isa=$3; opt=$4; shift 4
inc=$(riscv64-elf-gcc -print-file-name=include)
F="-DCTRL_REENTRY_ASSERT -mabi=ilp32 -ffreestanding -fno-builtin -nostdinc -isystem $inc $opt -DNDEBUG -std=c11 -Wall -Wextra -Werror -I$tree/include -I$tree/examples/rv32/include"
mkdir -p $out
riscv64-elf-gcc -march=$isa $F "$@" -c $tree/src/acmp.c -o $out/acmp.o
riscv64-elf-gcc -march=${isa}_zicsr $F "$@" -c $MEASURE_C -o $out/measure.o
riscv64-elf-gcc -march=$isa $F -c $tree/examples/rv32/runtime.c -o $out/runtime.o
riscv64-elf-gcc -march=rv32i -mabi=ilp32 -c $tree/examples/rv32/start.S -o $out/start.o
riscv64-elf-gcc -march=$isa -mabi=ilp32 -nostdlib -nostartfiles -T$tree/examples/rv32/link.ld -Wl,--no-undefined $out/start.o $out/measure.o $out/acmp.o $out/runtime.o -lgcc -o $out/measure.elf
riscv64-elf-size $out/acmp.o | tail -1 | awk '{print "acmp.o text " $1 " data " $2 " bss " $3}' > $out/acmp-size.txt
