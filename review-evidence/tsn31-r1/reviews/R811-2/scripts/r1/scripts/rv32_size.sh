#!/bin/sh
# usage: rv32_size.sh MAIN_TREE HEAD_TREE WORK -- text of src/acmp.c for RV32I at 16 (default) and 33 sinks.
M=$1 H=$2 W=$3; mkdir -p "$W"
riscv64-elf-gcc --version | head -1
for n in default 33; do for o in -Os -O2 -O3; do for t in main:$M head:$H; do
  d=""; [ $n = 33 ] && d="-DACMP_MAX_SINKS=33u"
  riscv64-elf-gcc -march=rv32i -mabi=ilp32 -ffreestanding -fno-builtin -nostdinc -isystem "$(riscv64-elf-gcc -print-file-name=include)" -std=c11 -Wall -Wextra -Werror \
    -DNDEBUG -DCTRL_REENTRY_ASSERT $d $o -I"${t#*:}/examples/rv32/include" -I"${t#*:}/include" \
    -c "${t#*:}/src/acmp.c" -o "$W/${t%%:*}$o$n.o" || echo "rc=$?"
  printf 'sinks=%-7s %s %-4s text=%s\n' $n $o "${t%%:*}" "$(riscv64-elf-size "$W/${t%%:*}$o$n.o" | awk 'NR==2{print $1}')"
done; done; done
